from aiogram import Dispatcher
from aiogram_dialog.setup import setup_dialogs
from . import bot_menu


def setup_dialogs2(dp: Dispatcher):
    for dialog in [*bot_menu.bot_menu_dialogs()]:
        dp.include_router(dialog)

    setup_dialogs(dp)
