from aiogram import types
from aiogram.dispatcher import filters
from loader import dp


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.CHANNEL), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def get_channel(message: types.Message):
    print(message.from_user.id)