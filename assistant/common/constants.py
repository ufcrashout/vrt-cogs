MODELS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-0125": 16385,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-16k-0301": 16384,
    "gpt-3.5-turbo-16k-0613": 16384,
    "gpt-3.5-turbo-instruct": 8192,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-vision-preview": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4o": 128000,
    "gpt-4o-2024-05-13": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
}
PRICES = {
    "gpt-3.5-turbo": [0.001, 0.0015],
    "gpt-3.5-turbo-0301": [0.0015, 0.002],
    "gpt-3.5-turbo-0613": [0.0015, 0.002],
    "gpt-3.5-turbo-1106": [0.001, 0.002],
    "gpt-3.5-turbo-0125": [0.0005, 0.0015],
    "gpt-3.5-turbo-16k": [0.003, 0.004],
    "gpt-3.5-turbo-16k-0301": [0.003, 0.004],
    "gpt-3.5-turbo-16k-0613": [0.003, 0.004],
    "gpt-3.5-turbo-instruct": [0.0015, 0.002],
    "gpt-3.5-turbo-instruct-0914": [0.0015, 0.002],
    "gpt-4": [0.03, 0.06],
    "gpt-4-0301": [0.03, 0.06],
    "gpt-4-0613": [0.03, 0.06],
    "gpt-4-turbo": [0.01, 0.03],
    "gpt-4-turbo-preview": [0.01, 0.03],
    "gpt-4-1106-preview": [0.01, 0.03],
    "gpt-4-0125-preview": [0.01, 0.03],
    "gpt-4-vision-preview": [0.01, 0.03],
    "gpt-4-1106-vision-preview": [0.01, 0.03],
    "gpt-4-turbo-2024-04-09": [0.01, 0.03],
    "gpt-4-32k": [0.06, 0.12],
    "gpt-4-32k-0301": [0.06, 0.12],
    "gpt-4o": [0.005, 0.015],
    "gpt-4o-2024-05-13": [0.005, 0.015],
    "gpt-4o-mini": [0.00015, 0.0006],
    "gpt-4o-mini-2024-07-18": [0.00015, 0.0006],
    "text-ada-001": [0.0004, 0.0016],
    "text-babbage-001": [0.0006, 0.0024],
    "text-curie-001": [0.003, 0.012],
    "text-davinci-002": [0.03, 0.12],
    "text-davinci-003": [0.03, 0.12],
    "code-davinci-002": [0.03, 0.12],
    "text-embedding-ada-002": [0.0001, 0.0001],
    "text-embedding-ada-002-v2": [0.0001, 0.0001],
    "text-embedding-3-small": [0.00002, 0.00002],
    "text-embedding-3-large": [0.00013, 0.00013],
}
SUPPORTS_SEED = [
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4-1106-vision-preview",
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
]
SUPPORTS_VISION = [
    "gpt-4-vision-preview",
    "gpt-4-1106-vision-preview",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
]
SUPPORTS_TOOLS = [
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
]
READ_EXTENSIONS = [
    ".txt",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".xml",
    ".html",
    ".ini",
    ".css",
    ".toml",
    ".md",
    ".ini",
    ".conf",
    ".config",
    ".cfg",
    ".go",
    ".java",
    ".c",
    ".php",
    ".swift",
    ".vb",
    ".xhtml",
    ".rss",
    ".css",
    ".asp",
    ".js",
    ".ts",
    ".cs",
    ".c++",
    ".cpp",
    ".cbp",
    ".h",
    ".cc",
    ".ps1",
    ".bat",
    ".batch",
    ".shell",
    ".env",
    ".sh",
    ".bat",
    ".pde",
    ".spec",
    ".sql",
]
REACT_SUMMARY_MESSAGE = """
You will be given a snippet of text, your job is to create a summary of the text to provide context for future conversations.

# RULES
- OUTPUT ONLY THE SUMMARY WITHOUT THE ORIGINAL TEXT OR EXTRA DIALOGUE FROM YOU.
- KEEP THE SUMMARY SHORT AND TO THE POINT.
"""
REACT_NAME_MESSAGE = """
You will be given a snippet of text, your job is to create a "Memory Name" for the given text to provide context for future conversations.

# RULES
- OUTPUT ONLY THE NAME WITHOUT THE ORIGINAL TEXT OR EXTRA DIALOGUE FROM YOU.
- KEEP THE NAME LESS THAN 3 WORDS AND LESS THAN 40 CHARACTERS.
"""

GENERATE_IMAGE = {
    "name": "generate_image",
    "description": "Use this to generate an image from a text prompt.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "A sentence or phrase that describes what you want to visualize, must be less than 1000 characters",
            },
            "quality": {
                "type": "string",
                "enum": ["standard", "hd"],
                "description": "The quality of the image, defaults to standard",
            },
            "style": {
                "type": "string",
                "enum": ["natural", "vivid"],
                "description": "Vivid leans toward more hyper-real and dramatic images. Natural creates more natural, less hyper-real looking images. Defaults to 'vivid'",
            },
            "size": {
                "type": "string",
                "enum": ["1024x1024", "1792x1024", "1024x1792"],
                "description": "The size of the image, defaults to 1024x1024",
            },
        },
        "required": ["prompt"],
    },
}

SEARCH_INTERNET = {
    "name": "search_internet",
    "description": "Use this to search the internet for information.",
    "parameters": {
        "type": "object",
        "properties": {
            "search_query": {
                "type": "string",
                "description": "a sentence or phrase that describes what you are looking for",
            },
            "amount": {
                "type": "integer",
                "description": "Max amount of search results to fetch. Defaults to 10",
            },
        },
        "required": ["search_query"],
    },
}

CREATE_MEMORY = {
    "name": "create_memory",
    "description": "Use this to remember information that you normally wouldnt have access to. Useful when someone corrects you, tells you something new, or tells you to remember something. Use the search_memories function first to ensure no duplicates are created.",
    "parameters": {
        "type": "object",
        "properties": {
            "memory_name": {
                "type": "string",
                "description": "A short name to describe the memory, perferrably less than 50 characters or 3 words tops",
            },
            "memory_text": {
                "type": "string",
                "description": "The information to remember, write as if you are informing yourself of the thing to remember, Make sure to include the context of the conversation as well as the answer or important information to be retained",
            },
        },
        "required": ["memory_name", "memory_text"],
    },
}
SEARCH_MEMORIES = {
    "name": "search_memories",
    "description": "Use this to find information about something, always use this if you are unsure about the answer to a question.",
    "parameters": {
        "type": "object",
        "properties": {
            "search_query": {
                "type": "string",
                "description": "a sentence or phrase that describes what you are looking for, this should be as specific as possible, it will be tokenized to find the best match with related embeddings.",
            },
            "amount": {
                "type": "integer",
                "description": "Max amount of memories to fetch. Defaults to 2",
            },
        },
        "required": ["search_query"],
    },
}
EDIT_MEMORY = {
    "name": "edit_memory",
    "description": "Use this to edit existing memories, useful for correcting inaccurate memories after making them. Use search_memories first if the memory you need to edit is not in the conversation.",
    "parameters": {
        "type": "object",
        "properties": {
            "memory_name": {
                "type": "string",
                "description": "The name of the memory entry, case sensitive",
            },
            "memory_text": {
                "type": "string",
                "description": "The new text that will replace the current content of the memory, this should reflect the old memory with the corrections",
            },
        },
        "required": ["memory_name", "memory_text"],
    },
}
LIST_MEMORIES = {
    "name": "list_memories",
    "description": "Get a list of all your available memories",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
