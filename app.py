import asyncio
import logging
import sys
from email.message import Message
from email.policy import default
from gc import callbacks

from os import getenv
from random import setstate
from sys import prefix

from aiogram import Bot, Dispatcher, html,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, Message, CallbackQuery, FSInputFile, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import Router
from typing import Any
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiohttp.web_fileresponse import content_type
from pyexpat.errors import messages
from setuptools.command.build import build
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext

from aiogram.types import ContentType

# Kontakt xabarlar uchun filtri yaratamiz


TOKEN = "6799931798:AAHKfYsQRGjq0sgnAy9pIN683SK05wpuiL8"

dp = Dispatcher()
router = Router()

class Person(StatesGroup):
    name = State()
    age = State()
    address = State()
    phone = State()
    ks = State()
    kurs = State()

class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: str


def keyboard():
    # Create a ReplyKeyboardMarkup instance with the type field
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="☎️Contakt yuborish☎️", request_contact=True)]
        ],
        resize_keyboard=True
    )

    return keyboard
def keyboard2():
    # Create a ReplyKeyboardMarkup instance with the type field
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'rganishni endi boshladim 😁" )],
            [KeyboardButton(text="O'rtacha 😊" )],
            [KeyboardButton(text="Yaxshi bilaman 👌" )]
        ],
        resize_keyboard=True
    )

    return keyboard

def keyboard3():
    # Create a ReplyKeyboardMarkup instance with the type field
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚜️\"504 Gateway Timeout\" - Pyton + Telegram bot kursi⚜️" )],
            [KeyboardButton(text="⚜️\"404 Not Found Kursi\" - Java Backend kursi⚜️" )],
            [KeyboardButton(text="⚜️\"401 Unauthorized\" - C# and .Net Backend and ... kursi⚜️" )]
        ],
        resize_keyboard=True
    )

    return keyboard
selected_kurs=""

def creat_keybord():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚜️\"504 Gateway Timeout\" - Pyton + Telegram bot kursi⚜️", callback_data=MyCallback(foo="504_kursi", bar="Pyton + Telegram bot kursi⚜").pack())],
        [InlineKeyboardButton(text="⚜️\"404 Not Found Kursi\" - Java Backend kursi⚜️", callback_data=MyCallback(foo="404_kursi", bar="Java Backend kursi⚜").pack())],
        [InlineKeyboardButton(text="⚜️\"401 Unauthorized\" - C# and .Net Backend and ... kursi⚜️", callback_data=MyCallback(foo="401_kursi", bar="C# and .Net Backend and ... kursi").pack())]
    ])
    return keyboard

keyboard_python = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📜Ro'yxatdan o'tish📜", callback_data=MyCallback(foo="royhat", bar="Python_kursi").pack())],
    [InlineKeyboardButton(text="🔙orqaga", callback_data=MyCallback(foo="menu", bar="42").pack())]
])

@router.callback_query(MyCallback.filter(F.foo == "royhat"))
async def goto(query: CallbackQuery, state: FSMContext) -> None:

    await query.message.answer("F.I.SH kiriting:")
    await state.set_state(Person.name)
    await query.answer(cache_time=30)

@router.message(StateFilter(Person.name))
async def name(msg: Message, state: FSMContext) -> None:
    await state.update_data(name=msg.text)
    await msg.answer("Yoshingizni kiriting:")
    await state.set_state(Person.age)

@router.message(StateFilter(Person.age))
async def age(msg: Message, state: FSMContext) -> None:
    await state.update_data(age=msg.text)
    await msg.answer("Manzilingizni kiriting:")
    await state.set_state(Person.address)

@router.message(StateFilter(Person.address))
async def addres(msg: Message, state: FSMContext) -> None:
    await state.update_data(address=msg.text)

    await msg.answer("Telefon raqamingizni kiriting yoki yuboring:", reply_markup=keyboard())
    await state.set_state(Person.phone)

@router.message(StateFilter(Person.phone) and F.contact)
async def phone(msg: Message, state: FSMContext) -> None:
    phone_number = msg.contact.phone_number
    await state.update_data(phone=phone_number)

    await msg.answer("Kampyuter savodxonligiz qay darajada.",reply_markup=keyboard3())
    await state.set_state(Person.kurs)

@router.message(StateFilter(Person.kurs))
async def kursss(msg:Message, state:FSMContext)->None:
    await state.update_data(kurs=msg.text)
    await msg.answer("Kampyuter savodxonligiz qay darajada.", reply_markup=keyboard2())
    await state.set_state(Person.ks)


@router.message(StateFilter(Person.ks))
async def phone(msg:Message, state:FSMContext)->None:
    await state.update_data(ks=msg.text)
    await msg.answer("Ro'yxatdan o'tish yakunlandi",reply_markup=ReplyKeyboardRemove())
    data=await state.get_data()
    txt=(f"Sizning Ma'lumotlaringiz\n"
         f"Ismingiz:\t {data.get('name')}\n"
         f"Yoshingiz:\t {data.get('age')}\n"
         f"Manzilingiz:\t {data.get('address')}\n"
         f"Telefon raqamingiz:\t {data.get('phone')}\n"
         f"Kampyuter savodxonlingiz:\t {data.get('ks')}\n"
         f"Tanlagan kursingiz:\t {data.get('kurs')}")
    await state.clear()
    await msg.answer(txt)
    await msg.answer("Siz bilan tez orada bog'lanamiz😊")
    txt=txt+"\n@"+msg.from_user.username
    bot=Bot(TOKEN)
    await bot.send_message(5806169847,txt)

@router.callback_query(MyCallback.filter(F.foo == "504_kursi"))
async def send_picture(callback_query: CallbackQuery, callback_data:MyCallback):
    selected_kurs=callback_data.bar
    photo_path = r"imags/img1.png"
    photo = FSInputFile(photo_path)
    await callback_query.message.answer_photo(photo, caption=f"⚜️\"504 Gateway Timeout\" - Pyton + Telegram bot kursi⚜️\n"
                                                             f" Ushbu kurs orqali siz python dasturlash tilini o'rganasiz. Python dasturlash tili yordamida siz web saytlar, telegram bot, suniy inteleg kabi loyihalarni yaratishingiz mumkin.\n"
                                              "Kursimiz quyidagilardan modullardan iborat.\n\n"
                                              "1. Modul: Python Dasturlash Tili Kirish\n"
                                              "2. Modul: Python Asosiy Sintaksisi\n"
                                              "3. Modul: Pythonda Nazorat Tuzilmalari\n"
                                              "4. Modul: Funktsiyalar\n"
                                              "5. Modul: Ma'lumot Tuzilmalari\n"
                                              "6. Modul: Fayllar bilan Ishlash\n"
                                              "7. Modul: Xatoliklarni Ushtirish va Debugging\n"
                                              "8. Modul: Modullar va Paketlar\n"
                                              "9. Modul: Pythonda OOP (Obyektga Yo‘naltirilgan Dasturlash)\n"
                                              "10. Modul: Aiogram va Telegram Botlari Kirish\n"
                                              "11. Modul: Xabarlar va Yordamchi Funksiyalar\n"
                                              "12. Modul: Komandalar va Handlerlar\n"
                                              "13. Modul: Botni Tashqi Xizmatlar bilan Integratsiya\n"
                                              "14. Modul: Xavfsizlik va Xatoliklarni Boshqarish\n"
                                              "15. Modul: Amaliy Loyihalar\n\n"
                                              "Quyidagi havola orqali ro'yxatdan o'ting va kelajak sari ilk qadamingizni qo'ying", reply_markup=keyboard_python)
    await callback_query.answer(cache_time=30)
    await callback_query.message.delete()

@router.callback_query(MyCallback.filter(F.foo == "404_kursi"))
async def send_picture(callback_query: CallbackQuery, callback_data:MyCallback):
    selected_kurs=callback_data.bar
    photo_path = r"imags/img2.png"
    photo = FSInputFile(photo_path)
    await callback_query.message.answer_photo(photo, caption="⚜️\"404 Not Found Kursi\" - Java Backend kursi⚜️\n.     "
                                                             "Ushbu kurs orqali siz Java dasturlash tilini o'rganasiz. Java dasturlash tili yordamida siz web saytlar, Kompyuter dasturlari, bank tizmi platformalarini yaratishingiz mumkin.\n"
                                              "Kursimiz quyidagilardan modullardan iborat.\n\n"
                                              "1. Modul: Java Backend Dasturlashga Kirish\n"
                                                             "2. Modul: Java Asoslari\n"
                                                             "3. Modul: OOP (Obyektga Yo‘naltirilgan Dasturlash)\n"
                                                             "4. Modul: Java Kolektsiyalar va Ma'lumot Tuzilmalari\n"
                                                             "5. Modul: Ma'lumotlar Bazasi bilan Ishlash\n"
                                                             "6. Modul: Spring Framework\n"
                                                             "7. Modul: RESTful Web Xizmatlar\n"
                                                             "8. Modul: Xavfsizlik va Avtorizatsiya\n"
                                                             "9. Modul: Ma'lumotlarni Kesh (Cache) va Performans\n"
                                                             "10. Modul: Testlash va Qayta Ishlash\n"
                                              "12. Modul: Amaliy Loyihalar\n\n"
                                              "Quyidagi havola orqali ro'yxatdan o'ting va kelajak sari ilk qadamingizni qo'ying", reply_markup=keyboard_python)
    await callback_query.answer(cache_time=30)
    await callback_query.message.delete()

@router.callback_query(MyCallback.filter(F.foo == "401_kursi"))
async def send_picture(callback_query: CallbackQuery, callback_data:MyCallback):
    selected_kurs=callback_data.bar
    photo_path = r"imags/img3.png"
    photo = FSInputFile(photo_path)
    await callback_query.message.answer_photo(photo, caption="️\"401 Unauthorized\" - C# and .Net Backend and Desktop kursi⚜️\n     "
                                                             "Ushbu kurs orqali siz C# dasturlash tilini o'rganasiz. C# dasturlash tili yordamida siz web saytlar, Kompyuter dasturlari, bank tizmi platformalarini, o'yinlar va boshqa dasturlarni yaratishingiz mumkin.\n"
                "Kursimiz quyidagilardan modullardan iborat.\n\n"
                "1. Modul: C# va .NET Asoslariga Kirish\n"
                "2. Modul: C# Asoslari\n"
                "3. Modul: OOP (Obyektga Yo‘naltirilgan Dasturlash)\n"
                "4. Modul: Ma'lumot Tuzilmalari va Kolektsiyalar\n"
                "5. Modul: Ma'lumotlar Bazasi bilan Ishlash\n"
                "6. Modul: ASP.NET Core Framework\n"
                "7. Modul: RESTful Web Xizmatlar va API\n"
                "8. Modul: Xavfsizlik va Avtorizatsiya\n"
                "9. Modul: Windows Forms Asoslari\n"
                "10. Modul: Formlar va Kontrollerlar\n"
                "11. Modul: Ma'lumotlarni Ko‘rsatish va Boshqarish\n"
                "12. Modul: Dialoglar va Xabarlar\n"
                "13. Modul: Ma'lumotlar Bazasi Bilan Integratsiya\n"
                "14. Modul: Formlararo O‘tish va Muloqot\n"
                "15. Modul: Amaliy Loyihalar\n\n"
                "Quyidagi havola orqali ro'yxatdan o'ting va kelajak sari ilk qadamingizni qo'ying", reply_markup=keyboard_python)
    await callback_query.answer(cache_time=30)
    await callback_query.message.delete()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"{message.from_user.full_name} kelajakni shakllantiruvchi bilimlar olamiga xush kelibsiz! Bizda siz uchun maxsus tayyorlangan bir nechta kurslar mavjud. Har bir kurs yangi darajaga ko'tarilish uchun imkoniyatni yaratadi! Ushbu kurs orqali siz o'z kasbingizni topishingiz mumkin.\n📚 Bizning kurslar:\n", reply_markup=creat_keybord())

@router.callback_query(MyCallback.filter(F.foo == "menu"))
async def send_picture(callback_query: CallbackQuery):
    await callback_query.message.answer("Kurslar ro'yxati", reply_markup=creat_keybord())
    await callback_query.answer(cache_time=30)
    await callback_query.message.delete()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router)
    await dp.start_polling(bot)
    bott=bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("bot.log"),
                            logging.StreamHandler(sys.stdout)
                        ]
                        )
    asyncio.run(main())
