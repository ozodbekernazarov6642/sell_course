from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

allow_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Roziman✅")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

phone_number_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish 🤳🏻", request_contact=True)
        ]
    ], resize_keyboard=True
)

description_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Biznes"),
            KeyboardButton(text="VIP")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

allow_keyboard_kr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Розиман✅")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

phone_number_keyboard_kr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Телефон рақамни юбориш 🤳🏻", request_contact=True)
        ]
    ], resize_keyboard=True
)

description_keyboard_kr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бизнес"),
            KeyboardButton(text="ВИП")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Lotin"),
            KeyboardButton(text="Кирил")
        ]
    ], resize_keyboard=True
)
