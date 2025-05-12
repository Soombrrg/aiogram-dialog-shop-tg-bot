import operator

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
                Const("Products 🍕"),
                id="catalog_st.catalog",
                on_click=selected.on_catalog,
            ),
            Button(Const("Cart 🛒"), id="cart_st.cart", on_click=selected.on_cart),
        ),
        Row(
            Button(Const("About ℹ️"), id="main_st.about", on_click=selected.to_state),
            Button(
                Const("Payment 💰"), id="main_st.payment", on_click=selected.to_state
            ),
        ),
        Button(Const("Delivery ⛵"), id="main_st.delivery", on_click=selected.to_state),
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
                Const("Meals"),
                id="catalog_st.meals",
                on_click=selected.on_chosen_category,
            ),
            Button(
                Const("Drinks"),
                id="catalog_st.drinks",
                on_click=selected.on_chosen_category,
            ),
        ),
        Row(
            Cancel(
                Const("<< Back"),
                id="main_st.main_menu",
            ),
            Button(Const("Cart 🛒"), id="cart_st.cart", on_click=selected.on_cart),
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


def prev_next_btn(id_str: str):
    return Row(
        Button(
            Const("<< Prev."),
            id=id_str + ".prev",
            on_click=selected.new_info,
        ),
        Button(
            Const("Next. >>"),
            id=id_str + ".next",
            on_click=selected.new_info,
        ),
    )


def product_info_keyboard():
    return Group(
        Row(
            Button(
                Const("Buy"),
                id="add_to_cart",
                on_click=selected.on_buy_product,
            ),
            Button(Const("Cart 🛒"), id="cart_st.cart", on_click=selected.on_cart),
        ),
        prev_next_btn("catalog_st.product_info"),
    )


def enter_amount_keyboard():
    return Group(
        Row(
            Button(Const("Delete"), id="delete", on_click=selected.delete_amount),
            Button(Const("-1"), id="minus", on_click=selected.change_amount),
            Button(Const("+1"), id="plus", on_click=selected.change_amount),
        ),
        prev_next_btn("cart_st.enter_amount"),
        Row(
            Back(Const("<<")),
            Button(Const("Buy"), id="buy", on_click=selected.on_confirm_buy),
        ),
    )
