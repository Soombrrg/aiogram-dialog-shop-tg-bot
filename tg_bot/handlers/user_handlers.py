import logging

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from tg_bot.misc.states import MainMenuStates

logger = logging.getLogger(__name__)


async def command_start(message: Message, dialog_manager: DialogManager):
    logger.debug("command_start ----------")
    await dialog_manager.start(MainMenuStates.main_menu)


def register_user_handlers(rt: Router) -> None:
    rt.message.register(command_start, CommandStart())


def user_router_configuration():
    user_router = Router()
    # user_private_router.message.filter(ChatTypeFilter(["private"])) # If needed division between bot users
    register_user_handlers(user_router)
    return user_router
