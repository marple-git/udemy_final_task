from aiogram.dispatcher.filters.state import StatesGroup, State


class Authorization(StatesGroup):
    code = State()


class AddItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()


class Advertisement(StatesGroup):
    message = State()


class BuyItem(StatesGroup):
    amount = State()
    shipping_address = State()
    payment = State()
