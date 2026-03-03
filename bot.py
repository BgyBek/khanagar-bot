import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ── Logging (very helpful when debugging) ────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Paste YOUR REAL BOT TOKEN here ───────────────────────────────────────
bot = Bot(token="8627766359:AAG7H3VVYerh3MttM41RJaFM6z2OmwXj96M")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# ── Main bottom menu ─────────────────────────────────────────────────────
def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🍳 Breakfast"))
    kb.add(KeyboardButton("🌙 Dinner"))
    kb.add(KeyboardButton("🍷 Drinks"))
    kb.add(KeyboardButton("ℹ️ About"))
    return kb


# ── Inline sub-menu for each category ────────────────────────────────────
def get_category_inline(category: str):
    builder = InlineKeyboardBuilder()

    if category == "breakfast":
        builder.button(text="Buffet items", callback_data="bf_buffet")
        builder.button(text="Hot from kitchen", callback_data="bf_hot")

    elif category == "dinner":
        builder.button(text="Starters",       callback_data="dn_starters")
        builder.button(text="Main dishes",    callback_data="dn_mains")
        builder.button(text="Desserts",       callback_data="dn_desserts")

    elif category == "drinks":
        builder.button(text="Signature Cocktails", callback_data="dr_cocktails")
        builder.button(text="Wine by the glass",   callback_data="dr_wine_glass")
        builder.button(text="Wine by the bottle",  callback_data="dr_wine_bottle")
        builder.button(text="Spirits",             callback_data="dr_spirits")
        builder.button(text="Beer / Cider / Soft", callback_data="dr_beer_soft")

    builder.adjust(1 if category in ["breakfast", "dinner"] else 2)
    builder.button(text="← Back to main", callback_data="back_main")

    return builder.as_markup()


# ── Start / Menu command ─────────────────────────────────────────────────
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Welcome to **KHANAGAR** at Big Sky Lodge, Terelj 🌄\n"
        "Great table under the big sky.\n\n"
        "Choose category:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )


# ── Category buttons (Breakfast / Dinner / Drinks) ───────────────────────
@dp.message_handler(text=["🍳 Breakfast", "🌙 Dinner", "🍷 Drinks"])
async def show_category(message: types.Message):
    if message.text == "🍳 Breakfast":
        text = "Breakfast menu coming soon..."
    elif message.text == "🌙 Dinner":
        text = "Dinner menu coming soon..."
    else:
        text = "Drinks menu coming soon..."
    await message.answer(text)

# ── All callback handling ─────────────────────────────────────────────────
@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    await call.message.edit_text("You selected something!")
    await call.answer()

    # ── Prepare common variables ─────────────────────────────────────────
    section_title = ""
    content = ""

    # Breakfast ───────────────────────────────────────────────────────────
    if data == "bf_buffet":
        section_title = "Buffet"
        content = (
            "Fresh bread & focaccia\n"
            "Mongolian clotted cream butter (Өрөм)\n"
            "Seasonal fruits\n"
            "Yogurt\n"
            "Granola\n"
            "Cereal\n"
            "Cheese selection\n"
            "Coffee / Tea / Milk\n"
            "Egg of your choice"
        )

    elif data == "bf_hot":
        section_title = "Hot from kitchen"
        content = (
            "Scallion fritters (Nogootoi boortsog) — ₮18,000\n"
            "Egg sandwich — ₮24,000\n"
            "Spring onion omelette — ₮26,000\n"
            "Butter pancakes — ₮28,000\n"
            "Ham & cheese toast — ₮30,000\n"
            "Eggs Benedict — ₮32,000"
        )

    # Dinner ──────────────────────────────────────────────────────────────
    elif data == "dn_starters":
        section_title = "Starters"
        content = (
            "Lamb dumplings in broth (Bansh) — ₮28,000\n"
            "Goat cheese with roasted beetroot — ₮32,000\n"
            "Prawn bisque — ₮34,000\n"
            "Burrata & tomatoes — ₮38,000"
        )

    elif data == "dn_mains":
        section_title = "Main dishes"
        content = (
            "Tsuiwan (Mongolian noodles) — ₮34,000\n"
            "Crispy lamb pastry – Signature — ₮42,000\n"
            "Khanagar pizza – Signature — ₮45,000\n"
            "Kung Pao chicken — ₮52,000\n"
            "Pumpkin tortellini — ₮62,000\n"
            "Roasted chicken thigh — ₮68,000\n"
            "Seared fish — ₮78,000\n"
            "Braised beef short rib — ₮85,000\n"
            "Grass-fed sirloin steak — ₮89,000\n"
            "Braised lamb shoulder (Korean style) — ₮92,000"
        )

    elif data == "dn_desserts":
        section_title = "Desserts"
        content = (
            "Camel milk ice cream — ₮24,000\n"
            "Goat milk crème brûlée — ₮26,000\n"
            "Khanagar cheesecake — ₮28,000"
        )

    # Drinks ──────────────────────────────────────────────────────────────
    elif data == "dr_cocktails":
        section_title = "Signature Cocktails"
        content = (
            "THE KHAN — Wild Turkey bourbon, smoked honey... — ₮38,000\n"
            "SILK ROAD — Hendrick's gin, elderflower, cucumber... — ₮38,000"
        )

    elif data == "dr_wine_glass":
        section_title = "Wine by the Glass (150 ml)"
        content = (
            "Fanagoria Sauvignon Blanc — ₮30,000\n"
            "Fanagoria Chardonnay — ₮34,000\n"
            "Fanagoria Cabernet Sauvignon — ₮32,000\n"
            "Fanagoria Merlot — ₮34,000\n"
            "Fanagoria Rosé — ₮30,000\n"
            "... more available"
        )

    elif data == "dr_wine_bottle":
        section_title = "Wine by the Bottle (750 ml)"
        content = (
            "Fanagoria Sauvignon Blanc — ₮150,000\n"
            "Fanagoria Chardonnay — ₮165,000\n"
            "Fanagoria Cabernet Sauvignon — ₮160,000\n"
            "Fanagoria Merlot — ₮165,000\n"
            "Fanagoria Cru Lermont Brut — ₮185,000\n"
            "... more sparkling & premium"
        )

    elif data == "dr_spirits":
        section_title = "Spirits (50 ml pour)"
        content = (
            "Glenmorangie Original 10 Year — ₮42,000\n"
            "Johnnie Walker Black Label — ₮38,000\n"
            "Jack Daniel's Old No. 7 — ₮35,000\n"
            "Hennessy VS — ₮45,000\n"
            "Grey Goose — ₮40,000\n"
            "... many more whiskies, cognacs, vodkas"
        )

    elif data == "dr_beer_soft":
        section_title = "Beer, Cider, Soft Drinks"
        content = (
            "Sengur Premium Lager (500ml) — ₮15,000\n"
            "Heineken (500ml) — ₮20,000\n"
            "Strongbow Apple Cider (330ml) — ₮18,000\n"
            "Coca-Cola / Sprite — ₮8,000\n"
            "Evian still (330ml) — ₮8,000\n"
            "Fresh Orange Juice — ₮12,000"
        )

    # ── Send result ──────────────────────────────────────────────────────
    if section_title:
        text = f"**{section_title}**\n\n{content}\n\n(GF) Gluten-free | (V) Vegetarian | (MF) Milk-free"
        await callback.message.edit_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_category_inline(data.split("_")[0])
        )
    else:
        await callback.message.edit_text("Section not implemented yet.")

    await callback.answer()


# ── Run bot ──────────────────────────────────────────────────────────────
async def main():
    logger.info("Khanagar Menu Bot is starting...")
    await dp.start_polling(
        bot,
        allowed_updates=["message", "callback_query"]
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
