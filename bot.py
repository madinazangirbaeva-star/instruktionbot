import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN, CHANNEL_USERNAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ─── Советы (случайные) ───────────────────────────────────────────────────────

СОВЕТЫ = [
    "Сделай одну маленькую задачу. Это лучше, чем ничего 💪",
    "Если не знаешь, что делать — выпей воды и открой список задач 💧",
    "Иногда план на день — просто пережить этот день 🌙",
]

# ─── Состояния ────────────────────────────────────────────────────────────────

class Form(StatesGroup):
    waiting_for_cry = State()

# ─── Клавиатура ───────────────────────────────────────────────────────────────

def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 О нас"), KeyboardButton(text="💡 Советы")],
            [KeyboardButton(text="😤 Крик души"), KeyboardButton(text="📢 Перейти в канал")],
        ],
        resize_keyboard=True
    )

# ─── Хэндлеры ─────────────────────────────────────────────────────────────────

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"Привет, {name}! 👋\n\n"
        "Я помощник канала Инструкция к жизни — здесь про опору в жизни:\n"
        "от бытовых лайфхаков до поддержки, когда руки опускаются.\n\n"
        "Можешь написать мне что угодно или выбери тему 👇",
        reply_markup=main_keyboard()
    )

@dp.message(F.text == "📖 О нас")
async def about(message: types.Message):
    await message.answer(
        "Если тебе кажется, что ты не справляешься — тебе не кажется 😳\n\n"
        "Иногда кажется, что всем вокруг выдали какую-то секретную методичку по взрослой жизни, а я в этот день просто прогулял 🌪\n\n"
        "Все вокруг как будто знают, как выбирать нормальные продукты, как не впадать в ступор при виде налоговой квитанции и как, черт возьми, снимать квартиру, чтобы тебя не кинули на залог.\n\n"
        "Если тебе знакома данная ситуация, то добро пожаловать в наш канал! Привет. Это «Инструкция к жизни, которой нет» 👋\n\n"
        "Название ироничное, но цель у нас вполне серьезная — перестать паниковать и начать потихоньку разбираться. Мы создали этот канал, потому что сами до смерти устали от неопределенности.\n\n"
        "О чем мы говорим:\n\n"
        "👩‍💻 Про бытовуху, которая пугает: как съехать от родителей и не разориться, как накопить на отпуск, если в кармане только вера в светлое будущее, и как подписывать договоры, чтобы не продать душу.\n\n"
        "😞 Про голову и чувства: что делать, когда кажется, что все успешнее тебя? Как пережить неловкость в компании? Как разрешить себе лениться?\n\n"
        "🤩 Про возможности: где учиться, как искать работу и как не упустить шансы.\n\n"
        "Взрослая жизнь — это не врожденный дар. Это навык. Как езда на велике: сначала больно и коленки в кровь, а потом ты просто едешь 🔥\n\n"
        "Давайте пробовать вместе?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")]
        ])
    )

@dp.message(F.text == "💡 Советы")
async def advice(message: types.Message):
    совет = random.choice(СОВЕТЫ)
    await message.answer(совет)

@dp.message(F.text == "😤 Крик души")
async def cry(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_cry)
    await message.answer("Расскажи — что случилось? Я слушаю 👂")

@dp.message(Form.waiting_for_cry)
async def handle_cry(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Я всё понимаю — держись. Главное выжить 💙\n\n"
        "И помни — ты не один. В канале много таких же людей 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")]
        ])
    )

@dp.message(F.text == "📢 Перейти в канал")
async def channel(message: types.Message):
    await message.answer(
        "Вот наш канал — там выходят статьи, лайфхаки и поддержка 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Инструкция к жизни", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")]
        ])
    )

# ─── Запуск ───────────────────────────────────────────────────────────────────

async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
