from aiogram import Dispatcher
from aiogram_dialog.setup import DialogRegistry, setup_dialogs
from . import bot_menu


def setup_dialogs2(dp: Dispatcher):
    registry = DialogRegistry(dp)
    for dialog in [*bot_menu.bot_menu_dialogs()]:
        dp.include_router(dialog)

    setup_dialogs(dp)
