import logging
from dataclasses import dataclass
from itertools import product
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Product:
    name: str
    product_id: int
    price: float
    stock: int


@dataclass
class Category:
    name: str
    category_id: int
    items: list[Product]


@dataclass
class Cart:
    # user_id: int # for dividing carts for each user
    items: list[Product]
    quantity_dict: dict[int, [int, float]]


class Repo:
    categories = []

    def __init__(self, test_data: dict = None):
        self.cart = Cart(items=[], quantity_dict={})

        for category in test_data.get("categories", []):
            self.categories.append(Category(**category))

        for product in test_data.get("products", []):
            category_name = product.pop("category_name")
            product = Product(**product)
            for category in self.categories:
                if category.name == category_name:
                    category.items.append(product)
                    break

    # if will be using more than 2 categories
    # for menu extension
    async def get_categories(self, session):
        # query = select(Categories.category_name, Categories.category_id)
        # result = await session.execute(query)
        # categories = result.execute().all()
        return self.categories

    async def get_product_s(self, session, category_name: str) -> list[Product]:
        # query = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.category_name == category_name)
        # result = await session.execute(query)
        # products = result.execute().all()
        for category in self.categories:
            if category.name.lower() == category_name:
                return category.items

    async def get_product(self, session, product_id: int) -> Product:
        # query = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.product_id == product_id)
        # result = await session.execute(query)
        # product = result.execute().all()
        for category in self.categories:
            for product in category.items:
                if product.product_id == int(product_id):
                    return product

    ################### Cart interaction
    # TODO Add individual carts for each user (using user_id)
    async def product_to_cart(self, session, product_id: int) -> str:
        # query = insert(Cart).values(
        #   select(Products.product_name, Products.product_id, Products.price, Products.stock).where(Products.product_id == product_id)
        # )
        # await session.execute(query)
        # await session.commit()
        for product_item in self.cart.items:
            if product_item.product_id == product_id:
                return product_item.name

        for category in self.categories:
            for product_item in category.items:
                if product_item.product_id == product_id:
                    self.cart.items.append(product_item)
                    self.cart.quantity_dict[int(product_id)] = [
                        1,
                        product_item.price,
                    ]
                    return product_item.name

    async def get_cart(self, session) -> Cart:
        # query = select(Cart)
        # result = await session.execute(query)
        # products = result.execute().all()

        return self.cart

    async def change_amount_db(self, session, product_id: int, amount: int):
        # query = update(Cart).where(Cart.items.product_id == product_id).values(
        #   quantity_dict.product_id[0]+=amount
        # )
        # await session.execute(query)
        # await session.commit()
        action = None
        for product_item in self.cart.items:
            if product_item.product_id == product_id:
                action = "changed"
                self.cart.quantity_dict.get(product_id)[0] += amount
                if self.cart.quantity_dict[product_id][0] == 0:
                    self.cart.quantity_dict.pop(product_id, None)
                    self.cart.items.remove(product_item)
                    action = "removed"
                    return action
        return action

    async def delete_amount_db(self, session, product_id: int):
        # query = delete(Cart).where(Cart.items.product_id == product_id)
        # await session.execute(query)
        # await session.commit()
        for product in self.cart.items:
            if product.product_id == product_id:
                self.cart.quantity_dict.pop(product_id, None)
                self.cart.items.remove(product)
        return True

    # TODO confirm_buy_window
    async def buy_product(self, session, product_id: int, amount: int) -> bool:
        # query = update(Products).where(Products.product_id == product_id).values(
        #   stock=Products.stock - amount
        # )
        # await session.execute(query)
        # await session.commit()
        for category in self.cart.items:
            for product_item in category.items:
                if product_item.product_id == product_id:
                    product_item.stock -= amount
                    return True
