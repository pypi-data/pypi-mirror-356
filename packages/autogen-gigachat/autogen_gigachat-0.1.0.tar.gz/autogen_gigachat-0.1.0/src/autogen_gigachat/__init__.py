import importlib.metadata

__version__ = importlib.metadata.version("autogen_gigachat")

from ._gigachat_client import (
    GigachatChatCompletionClient,
)
from .config import (
    GigachatClientConfigurationConfigModel,
    CreateArgumentsConfigModel,
)

__all__ = [
    "GigachatChatCompletionClient",
    "GigachatClientConfigurationConfigModel",
    "CreateArgumentsConfigModel",
]
