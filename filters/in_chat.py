from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from loader import db


class in_chat_db(BoundFilter):
    async def check(self, message: Message) -> bool:
        users_info = await db.select_all_users()
        for user in users_info:
            if user[0] == str(message.from_user.id):
                return False
            return True
        return False
