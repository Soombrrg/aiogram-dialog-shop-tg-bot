from aiogram_dialog import Dialog

from tg_bot.dialogs.bot_menu import user_windows


def bot_menu_dialogs():
    return [
        Dialog(
            user_windows.main_window(),  # main
            user_windows.about_window(),
            user_windows.payment_window(),
            user_windows.delivery_window(),
        ),
        Dialog(
            user_windows.catalog_window(),  # catalog_main
            user_windows.drinks_window(),
            user_windows.meals_window(),
            user_windows.product_info_window(),
        ),
        Dialog(
            user_windows.cart_window(),  # cart_main
            user_windows.enter_amount_window(),
            user_windows.confirm_buy_window(),
        ),
    ]
