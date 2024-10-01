import asyncio
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ContentType, Message, CallbackQuery
from pytz import timezone

from data import config
from data.config import ADMINS
from keyboards.inline.user_inline import price, make_confirmation_keyboard
from states.user_state import User_register
from keyboards.default.user_keyboard import allow_keyboard, phone_number_keyboard, description_keyboard
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state=User_register.all_states)
@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    s = 0
    all_user = await db.select_all_users()
    for user in all_user:
        if user[0] == str(message.from_user.id):
            await message.answer(text="Siz botdan ro'yxatdan o'tgansiz!\n\n"
                                      f"Ta'riflardan birni tanlang👇",
                                 reply_markup=description_keyboard)
            await User_register.description.set()
            s += 1
    if s == 0:
        await message.answer(
            f"Assalomu aleykum {message.from_user.full_name} Temuriy Avlodi universitetining to'lov botiga Xush kelibsiz")
        await message.answer("Sizga bir nechta savollar beraman, rozimisiz?\n\n"
                             "Rozi bo'lsangiz, pastdagi tugmani bosing❤️👇🏻", reply_markup=allow_keyboard)


@dp.message_handler(text="Roziman✅")
async def allow_user(message: types.Message):
    await message.answer(text="Ismingizni kiriting")
    await User_register.full_name.set()


@dp.message_handler(state=User_register.full_name)
async def full_name_user(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "full_name": message.text
        }
    )
    await message.answer("Telefon raqamingizni yuboring👇", reply_markup=phone_number_keyboard)
    await User_register.phone_number.set()


@dp.message_handler(state=User_register.phone_number, content_types=ContentType.CONTACT)
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
        phone_number= str(phone_number),
        date_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
        user_name=message.from_user.username
    )
    await message.answer("Ta'rifni tanlang", reply_markup=description_keyboard)
    await User_register.description.set()


@dp.message_handler(state=User_register.phone_number)
async def process_phone_number_test(message: Message, state: FSMContext):
    await message.answer(text="Telefon raqam yuborish tugmasini bo'sing👇")


@dp.message_handler(state=User_register.all_states, text="Yangi")
@dp.message_handler(text="Yangi")
async def process_description_new(message: Message, state: FSMContext):
    await state.update_data(
        {
            "description": message.text
        }
    )
    await message.answer(text="\t<b>🔰Yangi</b>\n\n"
                              "<b>Kurs narxi</b>👇\n"
                              "\t\t<i><b>370.000 so'm</b></i>\n\n"
                              "<b>Xususiyatlari</b>👇\n"
                              "\t\t<i><b>7 ta soha (xohishiy)✅</b></i>\n"
                              "\t\t<i><b>Kurator yordami✅</b></i>\n"
                              "\t\t<i><b>Guruh chat✅</b></i>\n"
                              "\t\t<i><b>Live vebinarlar✅</b></i>\n"
                              "\t\t<i><b>Individual darslar ❌</b></i>\n"
                              "\t\t<i><b>Sertifikat ❌</b></i>\n"
                              "\t\t<i><b>Coffee break ❌</b></i>\n"
                              "\t\t<i><b>Offline meeting❌</b></i>\n"
                              "\t\t<i><b>Investitsiya 30$❌</b></i>", reply_markup=price)
    await User_register.price.set()



@dp.message_handler(state=User_register.all_states, text="Qahramon")
@dp.message_handler(text="Qahramon")
async def process_description_standart(message: Message, state: FSMContext):
    await state.update_data(
        {
            "description": message.text
        }
    )
    await message.answer(text="\t<b>🔰Qahramon</b>\n\n"
                              "<b>Kurs narxi</b>👇\n"
                              "\t\t<i><b>597.000 so'm</b></i>\n"
                              "<b>Xususiyatlari</b>👇\n"
                              "\t\t<i><b>7 ta soha (xohishiy)✅</b></i>\n"
                              "\t\t<i><b>Kurator yordami✅</b></i>\n"
                              "\t\t<i><b>Guruh chat✅</b></i>\n"
                              "\t\t<i><b>Live vebinarlar✅</b></i>\n"
                              "\t\t<i><b>Individual darslar ✅</b></i>\n"
                              "\t\t<i><b>Sertifikat ✅</b></i>\n"
                              "\t\t<i><b>Coffee break ❌</b></i>\n"
                              "\t\t<i><b>Offline meeting❌</b></i>\n"
                              "\t\t<i><b>Investitsiya 30$❌</b></i>", reply_markup=price)
    await User_register.price.set()


@dp.callback_query_handler(text='price', state=User_register.price)
async def process_price(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="💳Karta ma'lumotlari:\n\n"
                                   "<b>Karta raqami</b>: <code>8600 0417 2124 4243</code>\n"
                                   "<b>Karta egasi</b>: <i>Nusratilla Sunnatullayev</i>\n\n"
                                   "Pul Miqdori to'g'riligini tekshiring va to'lov chekini skrinshotini shu yerga yuboring!")
    await User_register.check_state.set()


@dp.message_handler(state=User_register.check_state, content_types=types.ContentType.PHOTO)
async def process_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_info = await state.get_data()
    description = user_info["description"]
    user_all = await db.select_all_users()
    if description == "Qahramon":
        for user in user_all:
            if user[0] == str(message.from_user.id):
                await db.add_sell_course_user(
                    id=str(message.from_user.id),
                    phone_number=user[2],
                    full_name=user[1],
                    description=description,
                    course_sell_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
                    user_name=message.from_user.username,
                    price='597.000'
                )
                for user_ in await db.select_all_sell_course_users():
                    if user_[0] == user[0]:
                        await state.update_data(
                            {
                                "phone_number": user[2],
                                "full_name": user[1],
                                "data_time": user_[4],
                                'price': user_[6]
                            }
                        )
        user_info_1 = await state.get_data()
        await bot.send_photo(
            chat_id=config.ADMINS[0], photo=file_id, caption=(
                f"<b>Foydalanuvchi id</b>: <i>{message.from_user.id}\n</i>"
                f"<b>Telefon nomer</b>: <i>{user_info_1.get('phone_number')}\n</i>"
                f"<b>Foydalanuvchi Ismi</b>: <i>{user_info_1.get('full_name')}\n</i>"
                f"<b>Ta'rif</b>: <i>{user_info_1.get('description')}\n</i>"
                f"<b>To'lov summasi</b>: <i>{user_info_1.get('price')}\n</i>"
                f"<b>To'lov vaqti</b>:<i>{user_info_1.get('data_time')}\n </i>"
                f"<b>Foydalanuvchi nomi</b>:<i> <a href='https://t.me/{user_info_1.get('phone_number')}'>{message.from_user.full_name}</a></i>"
            ), reply_markup=await make_confirmation_keyboard(message.from_user.id)
        )

    if description == "Chempion":
        for user in user_all:
            if user[0] == str(message.from_user.id):
                await db.add_sell_course_user(
                    id=str(message.from_user.id),
                    phone_number=user[2],
                    full_name=user[1],
                    description=description,
                    course_sell_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
                    user_name=message.from_user.username,
                    price='1.200.000'
                )
                for user_ in await db.select_all_sell_course_users():
                    if user_[0] == user[0]:
                        await state.update_data(
                            {
                                "phone_number": user[2],
                                "full_name": user[1],
                                "data_time": user_[4],
                                'price': user_[6]
                            }
                        )
        user_info_1 = await state.get_data()
        await bot.send_photo(
            chat_id=config.ADMINS[0], photo=file_id, caption=(
                f"<b>Foydalanuvchi id</b>: <i>{message.from_user.id}\n</i>"
                f"<b>Telefon nomer</b>: <i>{user_info_1.get('phone_number')}\n</i>"
                f"<b>Foydalanuvchi Ismi</b>: <i>{user_info_1.get('full_name')}\n</i>"
                f"<b>Ta'rif</b>: <i>{user_info_1.get('description')}\n</i>"
                f"<b>To'lov summasi</b>: <i>{user_info_1.get('price')}\n</i>"
                f"<b>To'lov vaqti</b>:<i>{user_info_1.get('data_time')}\n </i>"
                f"<b>Foydalanuvchi nomi</b>:<i> <a href='https://t.me/{user_info_1.get('phone_number')}'>{message.from_user.full_name}</a></i>"
            ), reply_markup=await make_confirmation_keyboard(message.from_user.id)
        )


    if description == "Yangi":
        for user in user_all:
            if user[0] == str(message.from_user.id):
                await db.add_sell_course_user(
                    id=str(message.from_user.id),
                    phone_number=user[2],
                    full_name=user[1],
                    description=description,
                    course_sell_time=str(datetime.now(tz=timezone('Asia/Tashkent'))).split('.')[0],
                    user_name=message.from_user.username,
                    price='370.000'
                )
                for user_ in await db.select_all_sell_course_users():
                    if user_[0] == user[0]:
                        await state.update_data(
                            {
                                "phone_number": user[2],
                                "full_name": user[1],
                                "data_time": user_[4],
                                'price': user_[6]
                            }
                        )
        user_info_1 = await state.get_data()
        await bot.send_photo(
            chat_id=config.ADMINS[0], photo=file_id, caption=(
                f"<b>Foydalanuvchi id</b>: <i>{message.from_user.id}\n</i>"
                f"<b>Telefon nomer</b>: <i>{user_info_1.get('phone_number')}\n</i>"
                f"<b>Foydalanuvchi Ismi</b>: <i>{user_info_1.get('full_name')}\n</i>"
                f"<b>Ta'rif</b>: <i>{user_info_1.get('description')}\n</i>"
                f"<b>To'lov summasi</b>: <i>{user_info_1.get('price')}\n</i>"
                f"<b>To'lov vaqti</b>:<i>{user_info_1.get('data_time')}\n </i>"
                f"<b>Foydalanuvchi nomi</b>:<i> <a href='https://t.me/{user_info_1.get('phone_number')}'>{message.from_user.full_name}</a></i>"
            ), reply_markup=await make_confirmation_keyboard(message.from_user.id)
        )

    await message.answer("To'lovingiz haqida ma'lumot Menejerimizga yuborildi\n\n"
                         "To'lovingiz muvaffaqiyatli o'tgan bo'lsa 24 soat ichida sizga Menedjerlarimiz b   og'lanadi")
    await state.finish()
    await message.answer(text="Tanlovingiz uchun rahmat!\n\n"
                              "Hayotiy o'zgarishga tayyorlaning!✨✨✨")
    await asyncio.sleep(0.3)
    await message.answer("Ta'riflardan birni tanlang👇", reply_markup=description_keyboard)
    await User_register.description.set()


@dp.message_handler(state=User_register.all_states, text="Chempion")
@dp.message_handler(text="Chempion")
async def process_description_biznes(message: Message, state: FSMContext):
    await state.update_data(
        {
            "description": message.text
        }
    )
    await message.answer(text="\t<b>🔰Chempion</b>\n\n"
                              "<b>Kurs narxi</b>👇\n"
                              "\t\t<i><b>1.200.000 so'm</b></i>\n"
                              "<b>Xususiyatlari</b>👇\n"
                              "\t\t<i><b>7 ta soha (xohishiy)✅</b></i>\n"
                              "\t\t<i><b>Kurator yordami✅</b></i>\n"
                              "\t\t<i><b>Guruh chat✅</b></i>\n"
                              "\t\t<i><b>Live vebinarlar✅</b></i>\n"
                              "\t\t<i><b>Individual darslar ✅</b></i>\n"
                              "\t\t<i><b>Sertifikat ✅</b></i>\n"
                              "\t\t<i><b>Coffee break ✅</b></i>\n"
                              "\t\t<i><b>Offline meeting✅</b></i>\n"
                              "\t\t<i><b>Investitsiya 30$✅</b></i>", reply_markup=price)
    await User_register.price.set()


@dp.callback_query_handler(text="back_menu", state=User_register.all_states)
async def process_back_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Ta'rifni tanlang", reply_markup=description_keyboard)
    await User_register.description.set()
