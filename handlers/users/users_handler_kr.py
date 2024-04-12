from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType, Message, CallbackQuery
from pytz import timezone
from keyboards.inline.user_inline import price_kr, make_confirmation_keyboard_kr
from states.user_state import User_register_kr, User_lang
from keyboards.default.user_keyboard import description_keyboard_kr, allow_keyboard_kr, phone_number_keyboard_kr
from loader import dp, db, bot


@dp.message_handler(text="Кирил")
async def start_kiril(message: types.Message):
    s = 0
    all_user = await db.select_all_users()
    for user in all_user:
        if user[0] == str(message.from_user.id):
            await message.answer(text="Сиз ботдан рўйхатдан ўтгансиз!\n\n"
                                      f"Таърифлардан бирни танланг👇",
                                 reply_markup=description_keyboard_kr)
            await User_register_kr.description_kr.set()
            s += 1
    if s == 0:
        await message.answer("Ассалому алайкум!\n\n"
                             "Мен психолог Камола Шакарованинг ёрдамчиси <b>Меҳрибонман❤️</b>\n\n"
                             "Сизга МАТРИЦА трансформатсион дастурида қатнашишингиз учун ёрдам бераман!\n\n"
                             "Келинг, танишволамиз")
        await message.answer("Сизга бир нечта саволлар бераман, розимисиз?\n\n"
                             "Рози бўлсангиз, пастдаги тугмани босинг❤️👇🏻", reply_markup=allow_keyboard_kr)


@dp.message_handler(CommandStart(), state=User_register_kr.all_states)
async def cmd_start(message: types.Message):
    s = 0
    all_user = await db.select_all_users()
    for user in all_user:
        if user[0] == str(message.from_user.id):
            await message.answer(text="Сиз ботдан рўйхатдан ўтгансиз!\n\n"
                                      f"Таърифлардан бирни танланг👇",
                                 reply_markup=description_keyboard_kr)
            await User_register_kr.description_kr.set()
            s += 1
    if s == 0:
        await message.answer("Ассалому алайкум!\n\n"
                             "Мен психолог Камола Шакарованинг ёрдамчиси <b>Меҳрибонман❤️</b>\n\n"
                             "Сизга МАТРИЦА трансформатсион дастурида қатнашишингиз учун ёрдам бераман!\n\n"
                             "Келинг, танишволамиз")
        await message.answer("Сизга бир нечта саволлар бераман, розимисиз?\n\n"
                             "Рози бўлсангиз, пастдаги тугмани босинг❤️👇🏻", reply_markup=allow_keyboard_kr)


@dp.message_handler(text="Розиман✅")
async def allow_user(message: types.Message):
    await message.answer(text="Исмингизни киритинг")
    await User_register_kr.full_name_kr.set()


@dp.message_handler(state=User_register_kr.full_name_kr)
async def full_name_user(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "full_name": message.text
        }
    )
    await message.answer("Телефон рақамингизни юборинг👇", reply_markup=phone_number_keyboard_kr)
    await User_register_kr.phone_number_kr.set()


@dp.message_handler(state=User_register_kr.phone_number_kr, content_types=ContentType.CONTACT)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(
        {
            "phone_number": message.contact.phone_number
        }
    )
    user_info = await state.get_data()
    full_name_ = user_info["full_name"]
    phone_number = user_info["phone_number"]
    await db.add_user(
        id=str(message.from_user.id),
        full_name=full_name_,
        phone_number=str(phone_number),
        date_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
        user_name=message.from_user.username
    )
    await message.answer("Таърифни танланг", reply_markup=description_keyboard_kr)
    await User_register_kr.description_kr.set()


@dp.message_handler(state=User_register_kr.phone_number_kr)
async def process_phone_number_test(message: Message, state: FSMContext):
    await message.answer(text="Телефон рақам юбориш тугмасини бўсинг👇")


@dp.message_handler(state=User_register_kr.all_states, text="Бизнес")
@dp.message_handler(text="Бизнес")
async def process_description_standart(message: Message, state: FSMContext):
    await state.update_data(
        {
            "description": message.text
        }
    )
    await message.answer(text="\t<b>БИЗНЕС</b>\n\n"
                              "<b>Курс нархи</b> <i>999.000 сўм</i>\n", reply_markup=price_kr)
    await User_register_kr.price_kr.set()


@dp.callback_query_handler(text='price', state=User_register_kr.price_kr)
async def process_price(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="💳Карта маълумотлари:\n\n"
                                   "<b>Карта рақами</b>: <code>5614 6820 0657 7847</code>\n"
                                   "<b>Карта эгаси</b>: <i>Камола Шакарова</i>\n\n"
                                   "Пул Миқдори тўғрилигини текширинг ва тўлов чекини скриншотини шу ерга юборинг!")
    await User_register_kr.check_state_kr.set()


@dp.message_handler(state=User_register_kr.check_state_kr, content_types=types.ContentType.PHOTO)
async def process_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_info = await state.get_data()
    description = user_info["description"]
    user_all = await db.select_all_users()
    if description == 'Бизнес':
        for user in user_all:
            if user[0] == str(message.from_user.id):
                await db.add_sell_course_user(
                    id=str(message.from_user.id),
                    phone_number=user[2],
                    full_name=user[1],
                    description=description,
                    course_sell_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
                    price="999.000",
                    user_name=message.from_user.username
                )
                for user_ in await db.select_all_sell_course_users():
                    if user_[0] == user[0]:
                        await state.update_data(
                            {
                                "phone_number": user[2],
                                "full_name": user[1],
                                "data_time": user_[4],
                                "price": user_[6]
                            }
                        )
        user_info_1 = await state.get_data()
        await bot.send_photo(
            chat_id=6089744035, photo=file_id, caption=(
                f"<b>Foydalanuvchi id</b>: <i>{message.from_user.id}\n</i>"
                f"<b>Telefon nomer</b>: <i>{user_info_1.get('phone_number')}\n</i>"
                f"<b>Foydalanuvchi Ismi</b>: <i>{user_info_1.get('full_name')}\n</i>"
                f"<b>Ta'rif</b>: <i>{user_info_1.get('description')}\n</i>"
                f"<b>To'lov summasi</b>: <i>{user_info_1.get('price')}\n</i>"
                f"<b>To'lov vaqti</b>:<i>{user_info_1.get('data_time')}\n </i>"
                f"<b>Foydalanuvchi nomi</b>:<i> <a href='https://t.me/{user_info_1.get('phone_number')}'>{message.from_user.full_name}</a></i>"
            ), reply_markup=await make_confirmation_keyboard_kr(message.from_user.id)
        )
    if description == 'ВИП':
        for user in user_all:
            if user[0] == str(message.from_user.id):
                await db.add_sell_course_user(
                    id=str(message.from_user.id),
                    phone_number=user[2],
                    full_name=user[1],
                    description=description,
                    course_sell_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
                    price="5.555.000",
                    user_name=message.from_user.username
                )
                for user_ in await db.select_all_sell_course_users():
                    if user_[0] == user[0]:
                        await state.update_data(
                            {
                                "phone_number": user[2],
                                "full_name": user[1],
                                "data_time": user_[4],
                                "price": user_[6]
                            }
                        )
        user_info_1 = await state.get_data()
        await bot.send_photo(
            chat_id=6089744035, photo=file_id, caption=(
                f"<b>Foydalanuvchi id</b>: <i>{message.from_user.id}\n</i>"
                f"<b>Telefon nomer</b>: <i>{user_info_1.get('phone_number')}\n</i>"
                f"<b>Foydalanuvchi Ismi</b>: <i>{user_info_1.get('full_name')}\n</i>"
                f"<b>Ta'rif</b>: <i>{user_info_1.get('description')}\n</i>"
                f"<b>To'lov summasi</b>: <i>{user_info_1.get('price')}\n</i>"
                f"<b>To'lov vaqti</b>:<i>{user_info_1.get('data_time')}\n </i>"
                f"<b>Foydalanuvchi nomi</b>:<i> <a href='https://t.me/{user_info_1.get('phone_number')}'>{message.from_user.full_name}</a></i>"
            ), reply_markup=await make_confirmation_keyboard_kr(message.from_user.id)
        )
    await message.answer("Тўловингиз ҳақида маълумот Менежеримизга юборилди\n\n"
                         "Тўловингиз муваффақиятли ўтган бўлса 24 соат ичида сизга Менеджерларимиз Бот орқали ёпиқ гуруҳ линкини юборади!")
    await message.answer(text="Танловингиз учун раҳмат!\n\n"
                              "Ҳаётий трансформатсияларга тайёрланинг!✨✨✨")
    await message.answer("Таърифлардан бирни танланг👇", reply_markup=description_keyboard_kr)
    await User_register_kr.description_kr.set()


@dp.message_handler(state=User_register_kr.all_states, text="ВИП")
@dp.message_handler(text="ВИП")
async def process_description_biznes(message: Message, state: FSMContext):
    await state.update_data(
        {
            "description": message.text
        }
    )
    await message.answer(text="\t<b>ВИП</b>\n\n"
                              "<b>Курс нархи</b> <i>5.555.000 сўм</i>\n", reply_markup=price_kr)
    await User_register_kr.price_kr.set()


@dp.callback_query_handler(text="back_menu", state=User_register_kr.price_kr)
async def process_back_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Таърифни танланг", reply_markup=description_keyboard_kr)
    await User_register_kr.description_kr.set()
