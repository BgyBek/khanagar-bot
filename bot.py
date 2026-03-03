import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8627766359:AAG7H3VVYerh3MttM41RJaFM6z2OmwXj96M"  # ← Таны жинхэнэ токен

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Үндсэн bottom menu
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🍳 Breakfast")
    builder.button(text="🌙 Dinner")
    builder.button(text="🍷 Drinks & Cocktails")
    builder.button(text="ℹ️ About")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


# Category сонгоход гардаг inline menu
def get_category_inline(category: str):
    builder = InlineKeyboardBuilder()

    if category == "breakfast":
        builder.button(text="Buffet items", callback_data="bf_buffet")
        builder.button(text="Hot from kitchen", callback_data="bf_hot")

    elif category == "dinner":
        builder.button(text="Starters", callback_data="dn_starters")
        builder.button(text="Main dishes", callback_data="dn_mains")
        builder.button(text="Desserts", callback_data="dn_desserts")

    elif category == "drinks":
        builder.button(text="Signature Cocktails", callback_data="dr_cocktails")
        builder.button(text="Wine by the Glass (150ml)", callback_data="dr_wine_glass")
        builder.button(text="Wine by the Bottle (750ml)", callback_data="dr_wine_bottle")
        builder.button(text="Spirits (50ml pour)", callback_data="dr_spirits")
        builder.button(text="Beer / Cider / Soft Drinks", callback_data="dr_beer_soft")

    builder.button(text="← Back to main", callback_data="back_main")
    builder.adjust(1 if category in ["breakfast", "dinner"] else 2)

    return builder.as_markup()


# Бүх хэсгийн дэлгэрэнгүй button-уудыг гаргах функц
def get_submenu_inline(sub_category: str):
    builder = InlineKeyboardBuilder()

    if sub_category == "bf_hot":
        builder.button(text="Scallion fritters — ₮18,000", callback_data="item_bf_hot_scallion")
        builder.button(text="Egg sandwich — ₮24,000", callback_data="item_bf_hot_egg_sandwich")
        builder.button(text="Spring onion omelette — ₮26,000", callback_data="item_bf_hot_omelette")
        builder.button(text="Butter pancakes — ₮28,000", callback_data="item_bf_hot_pancakes")
        builder.button(text="Ham & cheese toast — ₮30,000", callback_data="item_bf_hot_toast")
        builder.button(text="Eggs Benedict — ₮32,000", callback_data="item_bf_hot_benedict")

    elif sub_category == "dn_starters":
        builder.button(text="Lamb Bansh — ₮28,000", callback_data="item_dn_starters_bansh")
        builder.button(text="Goat cheese & beetroot — ₮32,000", callback_data="item_dn_starters_beetroot")
        builder.button(text="Prawn bisque — ₮34,000", callback_data="item_dn_starters_bisque")
        builder.button(text="Burrata & tomatoes — ₮38,000", callback_data="item_dn_starters_burrata")

    elif sub_category == "dn_mains":
        builder.button(text="Tsui Van — ₮34,000", callback_data="item_dn_mains_tsui_van")
        builder.button(text="Crispy lamb pastry — ₮42,000", callback_data="item_dn_mains_lamb_pastry")
        builder.button(text="Khanagar pizza — ₮45,000", callback_data="item_dn_mains_pizza")
        builder.button(text="Kung Pao chicken — ₮52,000", callback_data="item_dn_mains_kungpao")
        builder.button(text="Pumpkin tortellini — ₮62,000", callback_data="item_dn_mains_tortellini")
        builder.button(text="Roasted chicken thigh — ₮68,000", callback_data="item_dn_mains_chicken")
        builder.button(text="Seared fish — ₮78,000", callback_data="item_dn_mains_fish")
        builder.button(text="Braised beef short rib — ₮85,000", callback_data="item_dn_mains_short_rib")
        builder.button(text="Grass-fed sirloin steak — ₮89,000", callback_data="item_dn_mains_steak")
        builder.button(text="Braised lamb shoulder — ₮92,000", callback_data="item_dn_mains_lamb_shoulder")

    elif sub_category == "dn_desserts":
        builder.button(text="Camel milk ice cream — ₮24,000", callback_data="item_dn_desserts_icecream")
        builder.button(text="Goat milk crème brûlée — ₮26,000", callback_data="item_dn_desserts_creme")
        builder.button(text="Khanagar cheesecake — ₮28,000", callback_data="item_dn_desserts_cheesecake")

    elif sub_category == "dr_cocktails":
        builder.button(text="THE KHAN — ₮38,000", callback_data="item_dr_cocktails_khan")
        builder.button(text="SILK ROAD — ₮38,000", callback_data="item_dr_cocktails_silkroad")

    elif sub_category == "dr_wine_glass":
        builder.button(text="Sauvignon Blanc — ₮30,000", callback_data="item_dr_wine_glass_sauvignon")
        builder.button(text="Chardonnay — ₮34,000", callback_data="item_dr_wine_glass_chardonnay")
        builder.button(text="Cabernet Sauvignon — ₮32,000", callback_data="item_dr_wine_glass_cabernet")
        builder.button(text="Merlot — ₮34,000", callback_data="item_dr_wine_glass_merlot")
        builder.button(text="Rosé — ₮30,000", callback_data="item_dr_wine_glass_rose")

    elif sub_category == "dr_wine_bottle":
        builder.button(text="Sauvignon Blanc — ₮150,000", callback_data="item_dr_wine_bottle_sauvignon")
        builder.button(text="Chardonnay — ₮165,000", callback_data="item_dr_wine_bottle_chardonnay")
        builder.button(text="Cabernet Sauvignon — ₮160,000", callback_data="item_dr_wine_bottle_cabernet")
        builder.button(text="Merlot — ₮165,000", callback_data="item_dr_wine_bottle_merlot")
        builder.button(text="Cru Lermont Brut — ₮185,000", callback_data="item_dr_wine_bottle_brut")

    elif sub_category == "dr_spirits":
        builder.button(text="Glenmorangie 10 Year — ₮42,000", callback_data="item_dr_spirits_glenmorangie")
        builder.button(text="Johnnie Walker Black — ₮38,000", callback_data="item_dr_spirits_johnnie")
        builder.button(text="Jack Daniel's No.7 — ₮35,000", callback_data="item_dr_spirits_jack")
        builder.button(text="Hennessy VS — ₮45,000", callback_data="item_dr_spirits_hennessy")

    elif sub_category == "dr_beer_soft":
        builder.button(text="Coca-Cola — ₮8,000", callback_data="item_dr_soft_coke")
        builder.button(text="Sprite — ₮8,000", callback_data="item_dr_soft_sprite")
        builder.button(text="Fanta Orange — ₮8,000", callback_data="item_dr_soft_fanta")
        builder.button(text="Sengur Lager — ₮15,000", callback_data="item_dr_soft_sengur")
        builder.button(text="Heineken — ₮20,000", callback_data="item_dr_soft_heineken")
        builder.button(text="Fresh Orange Juice — ₮12,000", callback_data="item_dr_soft_orange")

    builder.button(text="← Back", callback_data="back_" + sub_category.split("_")[0])
    builder.adjust(1)  # Нэг мөрөнд нэг button
    return builder.as_markup()


# Start / menu
@dp.message(CommandStart())
@dp.message(Command("menu"))
async def cmd_start_menu(message: Message):
    await message.answer(
        "Welcome to **KHANAGAR**\nBig Sky Lodge, Terelj 🌄\nGreat table under the big sky.\n\nChoose category:",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )


# Category handler
@dp.message(lambda m: m.text in ["🍳 Breakfast", "🌙 Dinner", "🍷 Drinks & Cocktails"])
async def show_category(message: Message):
    if "Breakfast" in message.text:
        title = "Breakfast (7:00 – 10:00)"
        cat = "breakfast"
    elif "Dinner" in message.text:
        title = "Dinner (18:00 – 22:00)"
        cat = "dinner"
    else:
        title = "Drinks & Beverages"
        cat = "drinks"

    await message.answer(
        f"**{title}**\nChoose section:",
        reply_markup=get_category_inline(cat),
        parse_mode=ParseMode.MARKDOWN
    )


# Callback handler (бүх button-ууд энд боловсруулагдана)
@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    data = callback.data

    if data == "back_main":
        await callback.message.edit_text("Буцлаа!")
        await callback.message.answer("Үндсэн menu:", reply_markup=get_main_menu())
        await callback.answer()
        return

    # Back to category
    if data.startswith("back_"):
        cat = data.split("_")[1]
        title = {
            "breakfast": "Breakfast (7:00 – 10:00)",
            "dinner": "Dinner (18:00 – 22:00)",
            "drinks": "Drinks & Beverages"
        }[cat]
        await callback.message.edit_text(
            f"**{title}**\nChoose section:",
            reply_markup=get_category_inline(cat),
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer()
        return

    # Item сонгосон үед
    if data.startswith("item_"):
        parts = data.split("_")
        section = parts[1]
        item = parts[2]

        item_name = {
            "bf_hot_scallion": "Scallion fritters (Nogootoi boortsog)",
            "bf_hot_egg_sandwich": "Egg sandwich",
            "bf_hot_omelette": "Spring onion omelette",
            "bf_hot_pancakes": "Butter pancakes",
            "bf_hot_toast": "Ham & cheese toast",
            "bf_hot_benedict": "Eggs Benedict",
            "dn_starters_bansh": "Lamb dumplings in broth (Bansh)",
            "dn_starters_beetroot": "Goat cheese with roasted beetroot",
            "dn_starters_bisque": "Prawn bisque",
            "dn_starters_burrata": "Burrata & tomatoes",
            "dn_mains_tsui_van": "Tsui Van (Mongolian noodles)",
            "dn_mains_lamb_pastry": "Crispy lamb pastry – Signature",
            "dn_mains_pizza": "Khanagar pizza – Signature",
            "dn_mains_kungpao": "Kung Pao chicken",
            "dn_mains_tortellini": "Pumpkin tortellini",
            "dn_mains_chicken": "Roasted chicken thigh",
            "dn_mains_fish": "Seared fish",
            "dn_mains_short_rib": "Braised beef short rib",
            "dn_mains_steak": "Grass-fed sirloin steak",
            "dn_mains_lamb_shoulder": "Braised lamb shoulder (Korean style)",
            "dn_desserts_icecream": "Camel milk ice cream",
            "dn_desserts_creme": "Goat milk crème brûlée",
            "dn_desserts_cheesecake": "Khanagar cheesecake",
            "dr_cocktails_khan": "THE KHAN",
            "dr_cocktails_silkroad": "SILK ROAD",
            "dr_wine_glass_sauvignon": "Fanagoria Sauvignon Blanc",
            "dr_wine_glass_chardonnay": "Fanagoria Chardonnay",
            "dr_wine_glass_cabernet": "Fanagoria Cabernet Sauvignon",
            "dr_wine_glass_merlot": "Fanagoria Merlot",
            "dr_wine_glass_rose": "Fanagoria Rosé",
            "dr_wine_bottle_sauvignon": "Fanagoria Sauvignon Blanc (bottle)",
            "dr_wine_bottle_chardonnay": "Fanagoria Chardonnay (bottle)",
            "dr_wine_bottle_cabernet": "Fanagoria Cabernet Sauvignon (bottle)",
            "dr_wine_bottle_merlot": "Fanagoria Merlot (bottle)",
            "dr_wine_bottle_brut": "Fanagoria Cru Lermont Brut",
            "dr_spirits_glenmorangie": "Glenmorangie Original 10 Year",
            "dr_spirits_johnnie": "Johnnie Walker Black Label",
            "dr_spirits_jack": "Jack Daniel's Old No. 7",
            "dr_spirits_hennessy": "Hennessy VS",
            "dr_soft_coke": "Coca-Cola",
            "dr_soft_sprite": "Sprite",
            "dr_soft_fanta": "Fanta Orange",
            "dr_soft_sengur": "Sengur Premium Lager",
            "dr_soft_heineken": "Heineken",
            "dr_soft_orange": "Fresh Orange Juice"
        }.get(item, "Unknown item")

        text = f"**{item_name}**\n\n" \
               "Үнэ: (дээрх жагсаалтаас харна уу)\n" \
               "Дэлгэрэнгүй мэдээлэл серверээс асууна уу.\n" \
               "Захиалах бол серверт хэлээрэй!"

        await callback.message.edit_text(text, reply_markup=get_submenu_inline(section))
        await callback.answer()
        return

    # Category submenu (жишээ: Hot from kitchen)
    if data in ["bf_hot", "dn_starters", "dn_mains", "dn_desserts", "dr_cocktails", "dr_wine_glass", "dr_wine_bottle", "dr_spirits", "dr_beer_soft"]:
        section_title = {
            "bf_hot": "Hot from kitchen",
            "dn_starters": "Starters",
            "dn_mains": "Main dishes",
            "dn_desserts": "Desserts",
            "dr_cocktails": "Signature Cocktails",
            "dr_wine_glass": "Wine by the Glass (150 ml)",
            "dr_wine_bottle": "Wine by the Bottle (750 ml)",
            "dr_spirits": "Spirits (50 ml pour)",
            "dr_beer_soft": "Beer, Cider, Soft Drinks"
        }[data]

        await callback.message.edit_text(
            f"**{section_title}**\nСонгоно уу:",
            reply_markup=get_submenu_inline(data),
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer()
        return

    await callback.message.edit_text("Сонгосон хэсэг: " + data)
    await callback.answer()


async def main():
    logger.info("Khanagar Menu Bot is starting...")
    await dp.start_polling(
        bot,
        allowed_updates=["message", "callback_query"]
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
