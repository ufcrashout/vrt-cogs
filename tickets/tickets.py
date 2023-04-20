import asyncio
import datetime
import logging

import discord
from discord.ext import tasks
from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n

from .abc import CompositeMetaClass
from .commands import TicketCommands
from .views import LogView, PanelView

log = logging.getLogger("red.vrt.tickets")
_ = Translator("Tickets", __file__)


# redgettext -D tickets.py base.py admin.py views.py menu.py
@cog_i18n(_)
class Tickets(TicketCommands, commands.Cog, metaclass=CompositeMetaClass):
    """
    Support ticket system with multi-panel functionality
    """

    __author__ = "Vertyco"
    __version__ = "1.11.31"

    def format_help_for_context(self, ctx):
        helpcmd = super().format_help_for_context(ctx)
        info = (
            f"{helpcmd}\n"
            f"Cog Version: {self.__version__}\n"
            f"Author: {self.__author__}\n"
        )
        return info

    async def red_delete_data_for_user(self, *, requester, user_id: int):
        """No data to delete"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(self, 117117, force_registration=True)
        default_guild = {
            # Settings
            "support_roles": [],  # Role ids
            "blacklist": [],  # User ids
            "max_tickets": 1,  # Max amount of tickets a user can have open at a time of any kind
            "inactive": 0,  # Auto close tickets with X hours of inactivity (0 = disabled)
            # Ticket data
            "opened": {},  # All opened tickets
            "panels": {},  # All ticket panels
            # Toggles
            "dm": False,
            "user_can_rename": False,
            "user_can_close": True,
            "user_can_manage": False,
            "transcript": False,
            "auto_add": False,  # Auto-add support/subroles to thread tickets
        }
        self.config.register_guild(**default_guild)

        self.ticket_panel_schema = {  # "panel_name" will be the key for the schema
            # Panel settings
            "category_id": 0,  # <Required>
            "channel_id": 0,  # <Required>
            "message_id": 0,  # <Required>
            # Button settings
            "button_text": "Open a Ticket",  # (Optional)
            "button_color": "blue",  # (Optional)
            "button_emoji": None,  # (Optional) Either None or an emoji for the button
            # Ticket settings
            "ticket_messages": [],  # (Optional) A list of messages to be sent
            "ticket_name": None,  # (Optional) Name format for the ticket channel
            "log_channel": 0,  # (Optional) Log open/closed tickets
            "modal": {},  # (Optional) Modal fields to fill out before ticket is opened
            "threads": False,  # Whether this panel makes a thread or channel
            "roles": [],  # Sub-support roles
            # Ticker
            "ticket_num": 1,
        }
        # v1.3.10 schema update (Modals)
        self.modal_schema = {
            "label": "",  # <Required>
            "style": "short",  # <Required>
            "placeholder": None,  # (Optional)
            "default": None,  # (Optional)
            "required": True,  # (Optional)
            "min_length": None,  # (Optional)
            "max_length": None,  # (Optional)
            "answer": None,  # (Optional)
        }

        self.valid = []  # Valid ticket channels

        self.auto_close.start()

    async def cog_load(self) -> None:
        asyncio.create_task(self.startup())

    async def cog_unload(self) -> None:
        self.auto_close.cancel()

    async def startup(self) -> None:
        await self.bot.wait_until_red_ready()
        await self.initialize()

    async def initialize(self, target_guild: discord.Guild = None) -> None:
        conf = await self.config.all_guilds()
        for gid, data in conf.items():
            if not data:
                continue
            if target_guild and target_guild.id != gid:
                continue
            guild = self.bot.get_guild(gid)
            if not guild:
                continue
            # Refresh buttons for all panels
            all_panels = data["panels"]
            to_deploy = {}  # Message ID keys for multi-button support
            for panel_name, panel in all_panels.items():
                catid = panel["category_id"]
                cid = panel["channel_id"]
                mid = panel["message_id"]
                if any([not catid, not cid, not mid]):
                    continue

                cat = guild.get_channel(catid)
                chan = guild.get_channel(cid)
                if any([not cat, not chan]):
                    continue

                try:
                    await chan.fetch_message(mid)
                except discord.NotFound:
                    continue
                except discord.Forbidden:
                    log.info(
                        f"I can no longer see a set panel channel in {guild.name}"
                    )
                    continue

                # v1.3.10 schema update (Modals)
                if "modals" not in panel:
                    panel["modals"] = {}

                panel["name"] = panel_name
                key = f"{cid}-{mid}"
                if key in to_deploy:
                    to_deploy[key].append(panel)
                else:
                    to_deploy[key] = [panel]

            if not to_deploy:
                continue

            try:
                for panels in to_deploy.values():
                    panelview = PanelView(self.bot, guild, self.config, panels)
                    await panelview.start()
            except discord.NotFound:
                log.warning(f"Failed to refresh panels in {guild.name}")

            # Refresh view for logs of opened tickets (v1.8.18 update)
            try:
                for opened_tickets in data["opened"].values():
                    for ticket_info in opened_tickets.values():
                        if not ticket_info["logmsg"]:
                            continue
                        panel_name = ticket_info["panel"]
                        panel = all_panels[panel_name]
                        if not panel["log_channel"]:
                            continue
                        channel = guild.get_channel(panel["log_channel"])
                        if not channel:
                            continue
                        try:
                            logmsg = await channel.fetch_message(
                                ticket_info["logmsg"]
                            )
                        except discord.NotFound:
                            log.warning(
                                f"Failed to get log channel message in {guild.name}"
                            )
                            continue
                        if not logmsg:
                            continue
                        view = LogView(guild, channel)
                        await logmsg.edit(view=view)
            except discord.NotFound:
                log.warning(f"Failed to refresh log views in {guild.name}")

    @tasks.loop(minutes=20)
    async def auto_close(self):
        actasks = []
        for guild in self.bot.guilds:
            await self.prune_invalid_tickets(guild)
            conf = await self.config.guild(guild).all()
            inactive = conf["inactive"]
            if not inactive:
                continue
            opened = conf["opened"]
            if not opened:
                continue
            for uid, tickets in opened.items():
                member = guild.get_member(int(uid))
                if not member:
                    continue
                for channel_id, ticket in tickets.items():
                    has_response = ticket.get("has_response")
                    if has_response and channel_id not in self.valid:
                        self.valid.append(channel_id)
                        continue
                    if channel_id in self.valid:
                        continue
                    channel = guild.get_channel(int(channel_id))
                    if not channel:
                        continue
                    now = datetime.datetime.now()
                    opened_on = datetime.datetime.fromisoformat(
                        ticket["opened"]
                    )
                    hastyped = await self.ticket_owner_hastyped(
                        channel, member
                    )
                    if hastyped and channel_id not in self.valid:
                        self.valid.append(channel_id)
                        continue
                    td = (now - opened_on).total_seconds() / 3600
                    next_td = td + 0.33
                    if td < inactive <= next_td:
                        # Ticket hasn't expired yet but will in the next loop
                        warning = _(
                            "If you do not respond to this ticket "
                            "within the next 20 minutes it will be closed automatically."
                        )
                        await channel.send(f"{member.mention}\n{warning}")
                        continue
                    elif td < inactive:
                        continue

                    time = "hours" if inactive != 1 else "hour"
                    try:
                        await self.close_ticket(
                            member,
                            channel,
                            conf,
                            _(
                                "(Auto-Close) Opened ticket with no response for "
                            )
                            + f"{inactive} {time}",
                            self.bot.user.name,
                        )
                        log.info(
                            f"Ticket opened by {member.name} has been auto-closed.\n"
                            f"Has typed: {hastyped}\n"
                            f"Hours elapsed: {td}"
                        )
                    except Exception as e:
                        log.error(
                            f"Failed to auto-close ticket for {member} in {guild.name}\nException: {e}"
                        )

        if tasks:
            await asyncio.gather(*actasks)

    @auto_close.before_loop
    async def before_auto_close(self):
        await self.bot.wait_until_red_ready()
        await asyncio.sleep(300)

    # Will automatically close/cleanup any tickets if a member leaves that has an open ticket
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if not member:
            return
        conf = await self.config.guild(member.guild).all()
        opened = conf["opened"]
        if str(member.id) not in opened:
            return
        tickets = opened[str(member.id)]
        if not tickets:
            return

        for cid in tickets:
            chan = self.bot.get_channel(int(cid))
            if not chan:
                continue
            try:
                await self.close_ticket(
                    member,
                    chan,
                    conf,
                    _("User left guild(Auto-Close)"),
                    self.bot.user.display_name,
                )
            except Exception as e:
                log.error(
                    f"Failed to auto-close ticket for {member} leaving {member.guild}\nException: {e}"
                )

    @commands.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):
        if not thread:
            return
        async with self.config.guild(thread.guild).all() as conf:
            for user_id, tickets in conf["opened"].items():
                for channel_id, ticket in tickets.items():
                    if channel_id != thread.id:
                        continue

                    panel = conf["panels"][ticket["panel"]]
                    log_message_id = ticket["logmsg"]
                    log_channel_id = panel["log_channel"]

                    if log_channel_id and log_message_id:
                        log_channel = thread.guild.get_channel(log_channel_id)
                        try:
                            log_message = await log_channel.fetch_message(
                                log_message_id
                            )
                            await log_message.delete()
                        except discord.NotFound:
                            pass

                    del conf["opened"][user_id][channel_id]
                    log.info(
                        f"Removed {thread.name} thread from config in {thread.guild.name}"
                    )
                    return
