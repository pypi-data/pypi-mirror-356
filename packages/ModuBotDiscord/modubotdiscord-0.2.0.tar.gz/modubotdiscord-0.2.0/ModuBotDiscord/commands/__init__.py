import functools
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, TypeVar

from discord import Interaction
from ModuBotDiscord.config import DiscordConfig

from ..enums import PermissionEnum

T = TypeVar("T", bound=Callable[..., Awaitable[None]])


async def send_message(
    interaction: Interaction, msg: str, ephemeral: bool = False
) -> None:
    if not interaction.response.is_done():
        await interaction.response.send_message(msg, ephemeral=ephemeral)
    else:
        await interaction.followup.send(msg, ephemeral=ephemeral)


async def send_error(
    interaction: Interaction, msg: str = "You are not allowed to use this command."
) -> None:
    await send_message(interaction, msg, True)


def check_permission(*permissions: PermissionEnum) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            missing = [
                perm.value
                for perm in permissions
                if not getattr(interaction.user.guild_permissions, perm.value, False)
            ]
            if missing:
                missing_permissions = ", ".join(f"`{m}`" for m in missing)
                await send_error(
                    interaction,
                    f"You are missing the following permissions: {missing_permissions}",
                )
                return None
            return await func(interaction, *args, **kwargs)

        return wrapper

    return decorator


def check_bot_permission(*permissions: PermissionEnum) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if not interaction.guild:
                await send_error(
                    interaction, "This command can only be used in a server."
                )
                return None

            bot_permissions = interaction.guild.me.guild_permissions
            missing = [
                perm.value
                for perm in permissions
                if not getattr(bot_permissions, perm.value, False)
            ]
            if missing:
                missing_permissions = ", ".join(f"`{m}`" for m in missing)
                await send_error(
                    interaction,
                    f"The bot is missing the following permissions: {missing_permissions}",
                )
                return None

            return await func(interaction, *args, **kwargs)

        return wrapper

    return decorator


def check_bot_owner() -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if interaction.user.id != DiscordConfig.OWNER_ID:
                await send_error(
                    interaction, "You must be the bot owner to use this command."
                )
                return None
            return await func(interaction, *args, **kwargs)

        return wrapper

    return decorator


def check_guild_owner() -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if (
                not interaction.guild
                or interaction.user.id != interaction.guild.owner_id
            ):
                await send_error(
                    interaction, "You must be the server owner to use this command."
                )
                return None
            return await func(interaction, *args, **kwargs)

        return wrapper

    return decorator


class BaseCommand(ABC):
    @abstractmethod
    async def register(self, bot: "ModuBotDiscord"):
        pass
