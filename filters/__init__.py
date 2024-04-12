from aiogram import Dispatcher

from loader import dp
# from .is_admin import AdminFilter
from .in_chat import in_chat_db

if __name__ == "filters":
    #dp.filters_factory.bind(is_admin)
    dp.filters_factory.bind(in_chat_db)
    pass
