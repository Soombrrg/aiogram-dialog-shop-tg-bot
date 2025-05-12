from aiogram.fsm.state import State, StatesGroup


# class AddBannerStates(StatesGroup):
#     image = State()
#
#
# class AddProductStates(StatesGroup):
#     # Шаги состояний
#     name = State()
#     description = State()
#     category = State()
#     price = State()
#     image = State()
#
#     product_for_change = None
#
#     texts = {
#         "AddProduct:name": "Введите название заново:",
#         "AddProduct:description": "Введите описание заново:",
#         "AddProduct:category": "Выберите категорию  заново ⬆️",
#         "AddProduct:price": "Введите стоимость заново:",
#         "AddProduct:image": "Этот стейт последний, поэтому...",
#     }


########################################################


### For DIALOG
class MainMenuStates(StatesGroup):
    main_menu = State()
    about = State()
    payment = State()
    delivery = State()


class CatalogStates(StatesGroup):
    catalog = State()
    drinks = State()
    meals = State()
    product_info = State()


class CartStates(StatesGroup):
    cart = State()
    enter_amount = State()
    confirm = State()


states = {
    "main_st": {
        "main_menu": MainMenuStates.main_menu,
        "about": MainMenuStates.about,
        "payment": MainMenuStates.payment,
        "delivery": MainMenuStates.delivery,
    },
    "catalog_st": {
        "catalog": CatalogStates.catalog,
        "drinks": CatalogStates.drinks,
        "meals": CatalogStates.meals,
        "product_info": CatalogStates.product_info,
    },
    "cart_st": {
        "cart": CartStates.cart,
        "enter_amount": CartStates.enter_amount,
        "confirm": CartStates.confirm,
    },
}
