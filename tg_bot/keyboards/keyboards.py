import operator

from aiogram.types import InlineKeyboardMarkup
from aiogram_dialog.widgets.kbd import (
    Group,
    Row,
    Button,
    Back,
    Cancel,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from tg_bot.dialogs.bot_menu import selected


SCROLLING_HEIGHT = 5


def main_menu_keyboard():
    return Group(
        Row(
            Button(
                Const("Товары 🍕"),
                id="catalog_st.catalog",
                on_click=selected.on_catalog,
            ),
            Button(Const("Корзина 🛒"), id="cart_st.cart", on_click=selected.on_cart),
        ),
        Row(
            Button(Const("О нас ℹ️"), id="main_st.about", on_click=selected.to_state),
            Button(
                Const("Оплата 💰"), id="main_st.payment", on_click=selected.to_state
            ),
        ),
        Button(Const("Доставка ⛵"), id="main_st.delivery", on_click=selected.to_state),
        id="menu_id",
    )


def back_btn():
    return Button(
        Const("<< Back"), id="main_st.main_menu", on_click=selected.to_state
    )  # Back(Const()) doesnt change photo back, because dialog_context


def catalog_keyboard():
    return Group(
        Row(
            Button(
                Const("Еда"),
                id="catalog_st.meals",
                on_click=selected.on_chosen_category,
            ),
            Button(
                Const("Напитки"),
                id="catalog_st.drinks",
                on_click=selected.on_chosen_category,
            ),
        ),
        Row(
            Cancel(
                Const("<< Back"),
                id="main_st.main_menu",
            ),
            Button(Const("Корзина 🛒"), id="cart_st.cart", on_click=selected.on_cart),
        ),
        id="catalog_id",
    )


def paginated_products(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="scroll_products",
            item_id_getter=operator.attrgetter("product_id"),
            items="products",
            on_click=on_click,
        ),
        id="products_id",
        width=1,
        height=SCROLLING_HEIGHT,
    )


def product_info_keyboard():
    return Group(
        Row(
            Button(
                Const("Купить"),
                id="add_to_cart",
                on_click=selected.on_buy_product,
            ),
            Button(Const("Корзина 🛒"), id="cart_st.cart", on_click=selected.on_cart),
        ),
        Row(
            Button(
                Const("<< Пред."),
                id="catalog_st.product_info.prev",
                on_click=selected.new_info,
            ),
            Button(
                Const("След. >>"),
                id="catalog_st.product_info.next",
                on_click=selected.new_info,
            ),
        ),
    )


def enter_amount_keyboard():
    return Group(
        Row(
            Button(Const("Удалить"), id="delete", on_click=selected.delete_amount),
            Button(Const("-1"), id="minus", on_click=selected.change_amount),
            Button(Const("+1"), id="plus", on_click=selected.change_amount),
        ),
        Row(
            Button(
                Const("<< Пред."),
                id="cart_st.enter_amount.prev",
                on_click=selected.new_info,
            ),
            Button(
                Const("След. >>"),
                id="cart_st.enter_amount.next",
                on_click=selected.new_info,
            ),
        ),
        Row(
            Back(Const("<<")),
        ),
    )


# def cart_keyboard():
#     return ScrollingGroup(
#         Select(
#             Format("{item.name}"),
#             id="scroll_products",
#             item_id_getter=operator.attrgetter("product_id"),
#             items="products",
#             on_click=on_click,
#         ),
#         id="products_id",
#         width=1,
#         height=SCROLLING_HEIGHT,
#     )
