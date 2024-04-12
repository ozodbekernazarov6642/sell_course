from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

price = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardMarkup(text="Bosh Menyu🏠", callback_data="back_menu"),
            InlineKeyboardButton(text="To'lov💳", callback_data="price")
        ]
    ]
)


async def make_confirmation_keyboard(user_id):
    confirmation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash✅", callback_data=f"con:{user_id}")
            ]
        ]
    )
    return confirmation_keyboard


confirmation_keyboard_price = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="To'lov Tasdiqlangan✅", callback_data=f"confirmation")
        ]
    ]
)

price_kr = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardMarkup(text="Бош Меню🏠", callback_data="back_menu"),
            InlineKeyboardButton(text="Тўлов💳", callback_data="price")
        ]
    ]
)


async def make_confirmation_keyboard_kr(user_id):
    confirmation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Тасдиқлаш✅", callback_data=f"con:{user_id}")
            ]
        ]
    )
    return confirmation_keyboard


confirmation_keyboard_price_kr = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Тўлов Тасдиқланган✅", callback_data=f"confirmation")
        ]
    ]
)
