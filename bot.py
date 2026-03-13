import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, GEMINI_API_KEY, CHANNEL_USERNAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""Ты — дружелюбный помощник Telegram-канала «Нам забыли выдать инструкцию» (@instruktionforlife).

Канал помогает людям разобраться во взрослой жизни: бытовые лайфхаки, финансовая грамотность, психологическая поддержка, карьера, отношения. Переводит сложное на понятный язык.

Твои правила:
1. Отвечай тепло, дружески, без пафоса — как умный друг, который разбирается в теме.
2. Если вопрос про финансы, быт, карьеру или отношения — давай практичный совет.
3. Если человек пишет, что ему плохо, руки опускаются, он устал или в кризисе — прежде всего выслушай и поддержи. Не торопись с советами. Напомни, что это нормально — просить помощь.
4. Периодически упоминай, что в канале @instruktionforlife есть статьи по теме — но ненавязчиво.
5. Не ставь диагнозов. При серьёзных психологических проблемах мягко рекомендуй обратиться к специалисту.
6. Отвечай на русском языке.
7. Не используй Markdown разметку — пиши обычным текстом без звёздочек и решёток.
8. Не пиши длинные простыни — будь кратким и по делу."""
)

chat_sessions: dict[int, any] = {}

def get_chat(user_id: int):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]

def clear_chat(user_id: int):
    chat_sessions[user_id] = model.start_chat(history=[])

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Финансы", callback_data="topic_finance"),
            InlineKeyboardButton(text="🏠 Быт", callback_data="topic_home"),
        ],
        [
            InlineKeyboardButton(text="💼 Карьера", callback_data="topic_career"),
            InlineKeyboardButton(text="❤️ Отношения", callback_data="topic_relations"),
        ],
        [
            InlineKeyboardButton(text="🧠 Мне сейчас плохо", callback_data="topic_support"),
        ],
        [
            InlineKeyboardButton(text="📢 Перейти в канал", url="https://t.me/instruktionforlife"),
        ],
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    clear_chat(message.from_user.id)
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"Привет, {name}! 👋\n\n"
        "Я помощник канала Нам забыли выдать инструкцию — здесь про опору в жизни:\n"
        "от бытовых лайфхаков до поддержки, когда руки опускаются.\n\n"
        "Можешь написать мне что угодно или выбери тему 👇",
        reply_markup=main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Я умею:\n"
        "• Отвечать на вопросы про финансы, быт, карьеру, отношения\n"
        "• Поддержать, если тяжело\n"
        "• Рекомендовать статьи из канала\n\n"
        "Просто напиши что тебя волнует 💬\n\n"
        "/start — начать заново\n"
        "/clear — очистить историю диалога",
        reply_markup=main_keyboard()
    )

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    clear_chat(message.from_user.id)
    await message.answer("История очищена. Начнём с чистого листа 🌱", reply_markup=main_keyboard())

@dp.callback_query(F.data.startswith("topic_"))
async def handle_topic(callback: types.CallbackQuery):
    topic_map = {
        "topic_finance": "Хочу разобраться с финансами. С чего начать?",
        "topic_home": "Помоги с бытовыми вопросами — есть полезные лайфхаки?",
        "topic_career": "Хочу поговорить про карьеру и работу.",
        "topic_relations": "Хочу поговорить про отношения.",
        "topic_support": "Мне сейчас плохо, руки опускаются.",
    }
    user_text = topic_map.get(callback.data, "Привет!")
    await callback.answer()
    await process_message(callback.message, callback.from_user.id, user_text)

@dp.message(F.text)
async def handle_text(message: types.Message):
    await process_message(message, message.from_user.id, message.text)

async def process_message(message: types.Message, user_id: int, user_text: str):
    await bot.send_chat_action(message.chat.id, "typing")
    chat = get_chat(user_id)
    try:
        response = await asyncio.to_thread(chat.send_message, user_text)
        reply_text = response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        reply_text = "Что-то пошло не так 😔 Попробуй чуть позже."
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Канал", url="https://t.me/instruktionforlife"),
         InlineKeyboardButton(text="🏠 Меню", callback_data="topic_menu")]
    ])
    await message.answer(reply_text, reply_markup=kb)

@dp.callback_query(F.data == "topic_menu")
async def handle_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выбери тему или просто напиши 👇", reply_markup=main_keyboard())

async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
