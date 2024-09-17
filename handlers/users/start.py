from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from states.user_state import User_register_kr, User_register
from filters import in_chat_db
from keyboards.default.user_keyboard import lang_keyboard
from loader import dp


@dp.message_handler(CommandStart(), state=User_register_kr.all_states)
@dp.message_handler(CommandStart(), state=User_register.all_states)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Salom, Botdan foydalanish uchun Tarifni tanlang", reply_markup=lang_keyboard)
    await state.finish()
