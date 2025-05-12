import logging

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from tg_bot.db.db_repo import Repo

logger = logging.getLogger(__name__)


async def get_image(dialog_manager: DialogManager, **middleware_data):
    context = dialog_manager.current_context()
    if not context.start_data:
        image_name = context.dialog_data.get("name", "main_menu")
    else:
        image_name = context.start_data.get("name")
    image_path = f"tg_bot/misc/images/{image_name}.jpeg"
    image = MediaAttachment(ContentType.PHOTO, path=image_path)

    return {"photo": image}


async def get_products_list(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    repo: Repo = middleware_data.get("repo")

    context = dialog_manager.current_context()
    category = context.dialog_data.get("name")

    image_path = f"tg_bot/misc/images/{category}.jpeg"
    image = MediaAttachment(ContentType.PHOTO, path=image_path)

    db_products = await repo.get_product_s(session, category)

    data = {"photo": image, "products": db_products}
    product_id_s = [product.product_id for product in db_products]

    context.dialog_data.update(amount=len(db_products), product_id_s=product_id_s)
    return data


# TODO product pictures
async def get_product_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    repo: Repo = middleware_data.get("repo")

    context = dialog_manager.current_context()
    product_id = int(context.dialog_data.get("product_id"))

    # image_path = f"tg_bot/misc/images/{category}.jpeg"
    # image = MediaAttachment(ContentType.PHOTO, path=image_path)

    product_info = await repo.get_product(session, product_id)

    # data = {"photo": image, "products": product_info}
    data = {"product": product_info}

    return data


async def get_cart_list(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    repo: Repo = middleware_data.get("repo")

    context = dialog_manager.current_context()
    image_name = "cart"
    # if not context.start_data:
    #     image_name = context.dialog_data.get("name", "cart")
    # else:
    #     image_name = context.start_data.get("name")
    image_path = f"tg_bot/misc/images/{image_name}.jpeg"
    image = MediaAttachment(ContentType.PHOTO, path=image_path)

    db_cart = await repo.get_cart(session)

    cart_ids = [product.product_id for product in db_cart.items]
    context.dialog_data.update(
        amount=len(db_cart.items),
        product_id_s=cart_ids,
        quantity_dict=db_cart.quantity_dict,
    )

    data = {"photo": image, "products": db_cart.items}
    return data


# TODO product pictures
async def get_buy_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get("session")
    repo: Repo = middleware_data.get("repo")

    context = dialog_manager.current_context()
    product_id = int(context.dialog_data.get("product_id"))

    product_info = []

    db_card = await repo.get_cart(session)
    for product in db_card.items:
        if product.product_id == product_id:
            product_info = product
            break

    quantity_dict = db_card.quantity_dict
    quantity = int(quantity_dict[product_id][0])

    products_cost = quantity * quantity_dict[product_id][1]
    total_cost = sum(product[0] * product[1] for product in quantity_dict.values())

    data = {
        "product": product_info,
        "total_cost": total_cost,
        "quantity": quantity,
        "products_cost": products_cost,
    }

    return data
