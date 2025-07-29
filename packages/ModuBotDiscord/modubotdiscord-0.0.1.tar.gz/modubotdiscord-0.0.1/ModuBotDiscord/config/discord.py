from typing import ClassVar
import os

from ModuBotCore.config import BaseConfig


class DiscordConfig(BaseConfig):
    TOKEN: ClassVar[str] = os.environ.get("DISCORD_TOKEN")
    OWNER_ID: ClassVar[int] = int(os.environ.get("DISCORD_OWNER_ID"))
