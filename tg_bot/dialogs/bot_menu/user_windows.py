################################ Main Menu Windows
from aiogram_dialog import Window, Data, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.bot_menu import getters, selected
from tg_bot.keyboards import keyboards
from tg_bot.misc.states import MainMenuStates, CatalogStates, CartStates


def main_window() -> Window:  # main
    return Window(
        DynamicMedia("photo"),
        Const("Добро пожаловать!"),
        keyboards.main_menu_keyboard(),
        state=MainMenuStates.main_menu,
        getter=getters.get_image,
    )


def about_window():
    return Window(
        DynamicMedia("photo"),
        Const("О нас!"),
        keyboards.back_btn(),
        state=MainMenuStates.about,
        getter=getters.get_image,
    )


def payment_window():
    return Window(
        DynamicMedia("photo"),
        Const("Оплата!"),
        keyboards.back_btn(),
        state=MainMenuStates.payment,
        getter=getters.get_image,
    )


def delivery_window():
    return Window(
        DynamicMedia("photo"),
        Const("Доставка!"),
        keyboards.back_btn(),
        state=MainMenuStates.delivery,
        getter=getters.get_image,
    )


################################ on_process_result
async def back_process_result(data: Data, result: dict, manager: DialogManager):
    await manager.switch_to(MainMenuStates.main_menu)


################################ Catalog Windows


# TODO: Любое количество категорий
def catalog_window():  # catalog_main
    return Window(
        DynamicMedia("photo"),
        Const("Категории:"),
        keyboards.catalog_keyboard(),
        state=CatalogStates.catalog,
        getter=getters.get_image,
    )


def drinks_window():
    return Window(
        DynamicMedia("photo"),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Const("<<")),
        state=CatalogStates.drinks,
        getter=getters.get_products_list,
    )


def meals_window():
    return Window(
        DynamicMedia("photo"),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Const("<<")),
        state=CatalogStates.meals,
        getter=getters.get_products_list,
    )


def product_info_window():
    return Window(
        # DynamicMedia("photo"),
        Format(
            """
Продукт: {product.name}
Цена: {product.price}
На складе: {product.stock}
"""
        ),
        keyboards.product_info_keyboard(),
        Back(Const("<<")),
        state=CatalogStates.product_info,
        getter=getters.get_product_info,
    )


################################ Cart Windows


def cart_window():  # cart_main
    return Window(
        DynamicMedia("photo"),
        Const("Корзина:"),
        keyboards.paginated_products(selected.on_buy_info),
        Cancel(
            Const("<< Back"),
        ),
        state=CartStates.cart,
        getter=getters.get_cart_list,
    )


# TODO product pictures
def enter_amount_window():
    return Window(
        # DynamicMedia("photo"),
        Format(
            """
Продукт: {product.name}
{product.price}$ x {quantity} = {products_cost}$
Общая стоимость товаров в корзине {total_cost}$
"""
        ),
        keyboards.enter_amount_keyboard(),
        state=CartStates.enter_amount,
        getter=getters.get_buy_info,
    )


# TODO confirm_buy_window
def confirm_buy_window():
    pass
