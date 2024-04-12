from aiogram.dispatcher.filters.state import StatesGroup, State


class User_register(StatesGroup):
    full_name = State()
    phone_number = State()
    description = State()
    price = State()
    check_state = State()


class User_register_kr(StatesGroup):
    full_name_kr = State()
    phone_number_kr = State()
    description_kr = State()
    price_kr = State()
    check_state_kr = State()


class User_lang(StatesGroup):
    latin = State()
    kiril = State()

