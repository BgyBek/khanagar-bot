# Импорт өөрчлөх
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Bot & Dispatcher үүсгэх
bot = Bot(token="YOUR_TOKEN")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Reply keyboard жишээ (main menu)
def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🍳 Breakfast"))
    kb.add(KeyboardButton("🌙 Dinner"))
    kb.add(KeyboardButton("🍷 Drinks"))
    kb.add(KeyboardButton("ℹ️ About"))
    return kb

# /start handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Welcome to **KHANAGAR** at Big Sky Lodge, Terelj 🌄\n"
        "Great table under the big sky.\n\n"
        "Choose category:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# Category handler (жишээ)
@dp.message_handler(text=["🍳 Breakfast", "🌙 Dinner", "🍷 Drinks"])
async def show_category(message: types.Message):
    if message.text == "🍳 Breakfast":
        text = "Breakfast menu coming soon..."
    elif message.text == "🌙 Dinner":
        text = "Dinner menu coming soon..."
    else:
        text = "Drinks menu coming soon..."
    await message.answer(text)

# Inline keyboard жишээ (callback)
@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    await call.message.edit_text("You selected something!")
    await call.answer()

# polling эхлүүлэх
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
