import asyncio
import multiprocessing as mp
import typing as t
from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path

import discord
from discord.ext.commands.cog import CogMeta
from redbot.core import commands
from redbot.core.bot import Red

from .common.models import DB, GuildSettings, Profile
from .generator.trustytenor.converter import TenorAPI


class CompositeMetaClass(CogMeta, ABCMeta):
    """Type detection"""


class MixinMeta(ABC):
    """Type hinting"""

    def __init__(self, *_args):
        self.bot: Red

        # Cache
        self.db: DB
        self.lastmsg: t.Dict[int, t.Dict[int, float]]
        self.in_voice: t.Dict[int, t.Dict[int, float]]
        self.profile_cache: t.Dict[int, t.Dict[int, t.Tuple[str, bytes]]]

        self.cog_path: Path
        self.bundled_path: Path
        # Custom
        self.custom_fonts: Path
        self.custom_backgrounds: Path
        # Bundled
        self.stock: Path
        self.fonts: Path
        self.backgrounds: Path

        # Save state
        self.saving = False
        self.last_save: float

        # Tenor
        self.tenor: TenorAPI

        # Internal API
        self.api_proc: t.Union[asyncio.subprocess.Process, mp.Process]

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_api(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def check_levelups(
        self,
        guild: discord.Guild,
        member: discord.Member,
        profile: Profile,
        conf: GuildSettings,
        message: t.Optional[discord.Message] = None,
        channel: t.Optional[
            t.Union[discord.TextChannel, discord.VoiceChannel, discord.Thread, discord.ForumChannel]
        ] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def initialize_voice_states(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def ensure_roles(
        self, member: discord.Member, conf: GuildSettings
    ) -> t.Tuple[t.List[discord.Role], t.List[discord.Role]]:
        raise NotImplementedError

    @abstractmethod
    async def get_banner(self, user_id: int) -> t.Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_profile_background(self, user_id: int, profile: Profile) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def get_user_profile(
        self, member: discord.Member, reraise: bool = False
    ) -> t.Union[discord.Embed, discord.File]:
        raise NotImplementedError

    @abstractmethod
    async def reset_weekly(self, guild: discord.Guild, ctx: commands.Context = None) -> None:
        raise NotImplementedError
