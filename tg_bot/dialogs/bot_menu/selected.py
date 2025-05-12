import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from tg_bot.db.db_repo import Repo
from tg_bot.misc.states import CartStates, CatalogStates, states

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


################################## Main
async def to_state(callback: CallbackQuery, widget: Button, manager: DialogManager):
    group, name = callback.data.split(".")

    context = manager.current_context()
    context.dialog_data.update(name=name)

    await manager.switch_to(states.get(group).get(name))


################################## Catalog
async def on_catalog(callback: CallbackQuery, widget: Button, manager: DialogManager):
    group, name = callback.data.split(".")

    await manager.start(states.get(group).get(name), data={"name": name})


# after choosing meals or drinks, saving category to dialog_data
async def on_chosen_category(
    callback: CallbackQuery, widget: Button, manager: DialogManager
):
    group, name = callback.data.split(".")

    context = manager.current_context()
    context.dialog_data.update(name=name)

    await manager.switch_to(states.get(group).get(name))


# list of products in category
async def on_chosen_product(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    context = manager.current_context()
    context.dialog_data.update(product_id=item_id)
    await manager.switch_to(CatalogStates.product_info)


async def on_buy_product(
    callback: CallbackQuery, widget: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    session = manager.middleware_data.get("session")
    context = manager.current_context()
    product_id = context.dialog_data.get("product_id")

    product_name = await repo.product_to_cart(session, int(product_id))
    await callback.answer(f"Added to cart {product_name}")


# To switch between Next Prev
async def new_info(callback: CallbackQuery, widget: Button, manager: DialogManager):
    group, name, action = callback.data.split(".")

    context = manager.current_context()
    product_id = int(context.dialog_data.get("product_id"))

    id_index = context.dialog_data.get("product_id_s").index(product_id)
    amount = context.dialog_data.get("amount")

    change = -1 if action == "prev" else 1
    id_index = id_index + change

    # cycling list
    if amount - 1 < id_index:
        id_index = 0
    if 0 > id_index > -amount:
        id_index = -1

    product_id = context.dialog_data.get("product_id_s")[id_index]
    context.dialog_data.update(product_id=product_id)

    await manager.switch_to(states.get(group).get(name))


################################## Cart
async def on_cart(callback: CallbackQuery, widget: Button, manager: DialogManager):
    group, name = callback.data.split(".")

    await manager.start(states.get(group).get(name), data={"name": name})


async def on_buy_info(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    context = manager.current_context()
    context.dialog_data.update(product_id=item_id)
    await manager.switch_to(CartStates.enter_amount)


async def change_amount(
    callback: CallbackQuery, widget: Button, manager: DialogManager
):
    action = callback.data

    amount = {"minus": -1, "plus": 1}.get(action, 0)

    repo: Repo = manager.middleware_data.get("repo")
    session = manager.middleware_data.get("session")

    context = manager.current_context()
    product_id = context.dialog_data.get("product_id")
    action = await repo.change_amount_db(session, int(product_id), amount)

    if action == "changed":
        await callback.answer("Quantity changed!")
    if action == "removed":
        await callback.answer("Removed from cart!")
        await manager.switch_to(CartStates.cart)


async def delete_amount(
    callback: CallbackQuery, widget: Button, manager: DialogManager
):
    repo: Repo = manager.middleware_data.get("repo")
    session = manager.middleware_data.get("session")

    context = manager.current_context()
    product_id = context.dialog_data.get("product_id")
    is_deleted = await repo.delete_amount_db(session, int(product_id))
    if is_deleted:
        await callback.answer("Removed from cart!")
        await manager.switch_to(CartStates.cart)


# TODO Buying products
async def on_confirm_buy(
    callback: CallbackQuery, widget: Button, manager: DialogManager
):
    await manager.switch_to(CartStates.confirm)
