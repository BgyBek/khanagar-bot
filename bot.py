import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update, Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8627766359:AAG7H3VVYerh3MttM41RJaFM6z2OmwXj96M"
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI(title="Khanagar Bot Webhook")

# Main bottom menu
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🍳 Breakfast")
    builder.button(text="🌙 Dinner")
    builder.button(text="🍷 Drinks & Cocktails")
    builder.button(text="ℹ️ About")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Inline category menu
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

    builder.adjust(2)
    builder.button(text="← Back to main", callback_data="back_main")

    return builder.as_markup()


# ── Submenu with individual item buttons ─────────────────────────────────
def get_item_inline(section: str):
    builder = InlineKeyboardBuilder()

    if section == "bf_buffet":
        builder.button(text="Fresh bread & focaccia", callback_data="item_bf_buffet_bread")
        builder.button(text="Mongolian clotted cream butter (Өрөм)", callback_data="item_bf_buffet_orem")
        builder.button(text="Seasonal fruits", callback_data="item_bf_buffet_fruits")
        builder.button(text="Yogurt", callback_data="item_bf_buffet_yogurt")
        builder.button(text="Granola", callback_data="item_bf_buffet_granola")
        builder.button(text="Cereal", callback_data="item_bf_buffet_cereal")
        builder.button(text="Cheese selection", callback_data="item_bf_buffet_cheese")
        builder.button(text="Coffee / Tea / Milk", callback_data="item_bf_buffet_drinks")
        builder.button(text="Egg of your choice", callback_data="item_bf_buffet_egg")

    elif section == "bf_hot":
        builder.button(text="Scallion fritters — ₮18,000", callback_data="item_bf_hot_scallion")
        builder.button(text="Egg sandwich — ₮24,000", callback_data="item_bf_hot_egg_sandwich")
        builder.button(text="Spring onion omelette — ₮26,000", callback_data="item_bf_hot_omelette")
        builder.button(text="Butter pancakes — ₮28,000", callback_data="item_bf_hot_pancakes")
        builder.button(text="Ham & cheese toast — ₮30,000", callback_data="item_bf_hot_toast")
        builder.button(text="Eggs Benedict — ₮32,000", callback_data="item_bf_hot_benedict")

    elif section == "dn_starters":
        builder.button(text="Lamb Bansh — ₮28,000", callback_data="item_dn_starters_bansh")
        builder.button(text="Goat cheese & beetroot — ₮32,000", callback_data="item_dn_starters_beetroot")
        builder.button(text="Prawn bisque — ₮34,000", callback_data="item_dn_starters_bisque")
        builder.button(text="Burrata & tomatoes — ₮38,000", callback_data="item_dn_starters_burrata")

    elif section == "dn_mains":
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

    elif section == "dn_desserts":
        builder.button(text="Camel milk ice cream — ₮24,000", callback_data="item_dn_desserts_icecream")
        builder.button(text="Goat milk crème brûlée — ₮26,000", callback_data="item_dn_desserts_creme")
        builder.button(text="Khanagar cheesecake — ₮28,000", callback_data="item_dn_desserts_cheesecake")

    elif section == "dr_cocktails":
        builder.button(text="THE KHAN — ₮38,000", callback_data="item_dr_cocktails_khan")
        builder.button(text="SILK ROAD — ₮38,000", callback_data="item_dr_cocktails_silkroad")

    elif section == "dr_wine_glass":
        builder.button(text="Sauvignon Blanc — ₮30,000", callback_data="item_dr_wine_glass_sauvignon")
        builder.button(text="Chardonnay — ₮34,000", callback_data="item_dr_wine_glass_chardonnay")
        builder.button(text="Cabernet Sauvignon — ₮32,000", callback_data="item_dr_wine_glass_cabernet")
        builder.button(text="Merlot — ₮34,000", callback_data="item_dr_wine_glass_merlot")
        builder.button(text="Rosé — ₮30,000", callback_data="item_dr_wine_glass_rose")

    elif section == "dr_wine_bottle":
        builder.button(text="Sauvignon Blanc — ₮150,000", callback_data="item_dr_wine_bottle_sauvignon")
        builder.button(text="Chardonnay — ₮165,000", callback_data="item_dr_wine_bottle_chardonnay")
        builder.button(text="Cabernet Sauvignon — ₮160,000", callback_data="item_dr_wine_bottle_cabernet")
        builder.button(text="Merlot — ₮165,000", callback_data="item_dr_wine_bottle_merlot")
        builder.button(text="Cru Lermont Brut — ₮185,000", callback_data="item_dr_wine_bottle_brut")

    elif section == "dr_spirits":
        builder.button(text="Glenmorangie 10 Year — ₮42,000", callback_data="item_dr_spirits_glenmorangie")
        builder.button(text="Johnnie Walker Black — ₮38,000", callback_data="item_dr_spirits_johnnie")
        builder.button(text="Jack Daniel's No.7 — ₮35,000", callback_data="item_dr_spirits_jack")
        builder.button(text="Hennessy VS — ₮45,000", callback_data="item_dr_spirits_hennessy")

    elif section == "dr_beer_soft":
        builder.button(text="Coca-Cola — ₮8,000", callback_data="item_dr_soft_coke")
        builder.button(text="Coca-Cola Zero — ₮8,000", callback_data="item_dr_soft_coke_zero")
        builder.button(text="Sprite — ₮8,000", callback_data="item_dr_soft_sprite")
        builder.button(text="Fanta Orange — ₮8,000", callback_data="item_dr_soft_fanta")
        builder.button(text="Sengur Premium Lager — ₮15,000", callback_data="item_dr_soft_sengur")
        builder.button(text="Heineken — ₮20,000", callback_data="item_dr_soft_heineken")
        builder.button(text="Fresh Orange Juice — ₮12,000", callback_data="item_dr_soft_orange")

    builder.button(text="← Back", callback_data="back_" + section.split("_")[0])
    builder.adjust(1)
    return builder.as_markup()


# ── Start / Menu command ─────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start_menu(message: Message):
    await message.answer(
        "Welcome to **KHANAGAR**\n"
        "Big Sky Lodge, Terelj 🌄\n"
        "Great table under the big sky.\n\n"
        "Choose category:",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )


# ── Category buttons handler ─────────────────────────────────────────────
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


# ── Callback handler ─────────────────────────────────────────────────────
@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    data = callback.data

    if data == "back_main":
        try:
            await callback.message.delete()
        except Exception:
            pass

        await callback.message.answer(
            "Main Menu:",
            reply_markup=get_main_menu(),
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer("Back to main")
        return

    if data.startswith("back_"):
        try:
            cat = data.split("_")[1]
        except IndexError:
            cat = "breakfast"

        title_map = {
            "breakfast": "Breakfast (7:00 – 10:00)",
            "dinner": "Dinner (18:00 – 22:00)",
            "drinks": "Drinks & Beverages"
        }

        title = title_map.get(cat, "Menu")

        await callback.message.edit_text(
            f"**{title}**\nChoose section:",
            reply_markup=get_category_inline(cat),
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer("Back to category")
        return

    if data == "bf_buffet":
        text = (
            "**Buffet Items**\n\n"
            "Fresh bread & focaccia\n"
            "Mongolian clotted cream butter (Өрөм)\n"
            "Seasonal fruits\n"
            "Yogurt\n"
            "Granola\n"
            "Cereal\n"
            "Cheese selection\n"
            "Coffee / Tea / Milk\n"
            "Egg of your choice\n\n"
        )
        await callback.message.edit_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_category_inline("breakfast")
        )
        await callback.answer()
        return

    sections = {
        "bf_buffet": ("Buffet Items", "bf_buffet"),
        "bf_hot": ("Hot from kitchen", "bf_hot"),
        "dn_starters": ("Starters", "dn_starters"),
        "dn_mains": ("Main dishes", "dn_mains"),
        "dn_desserts": ("Desserts", "dn_desserts"),
        "dr_cocktails": ("Signature Cocktails", "dr_cocktails"),
        "dr_wine_glass": ("Wine by the Glass (150 ml)", "dr_wine_glass"),
        "dr_wine_bottle": ("Wine by the Bottle (750 ml)", "dr_wine_bottle"),
        "dr_spirits": ("Spirits (50 ml pour)", "dr_spirits"),
        "dr_beer_soft": ("Beer, Cider, Soft Drinks", "dr_beer_soft"),
    }

    if data in sections:
        title, section = sections[data]
        await callback.message.edit_text(
            f"**{title}**\nSelect item:",
            reply_markup=get_item_inline(section),
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer()
        return

    if data.startswith("item_"):
        item_full_key = data.replace("item_", "")

        item_info = {
            "bf_buffet_fresh_bread": "Fresh bread & focaccia",
            "bf_buffet_clotted_cream": "Mongolian clotted cream butter (Өрөм)",
            "bf_buffet_fruits": "Seasonal fruits",
            "bf_buffet_yogurt": "Yogurt",
            "bf_buffet_granola": "Granola",
            "bf_buffet_cereal": "Cereal",
            "bf_buffet_cheese": "Cheese selection",
            "bf_buffet_coffee": "Coffee / Tea / Milk",
            "bf_buffet_egg": "Egg of your choice",

            "bf_hot_scallion": "Scallion fritters (Nogootoi boortsog) — ₮18,000\nServed with sour cream",
            "bf_hot_egg_sandwich": "Egg sandwich — ₮24,000\nSoft bread, creamy egg filling, herbs",
            "bf_hot_omelette": "Spring onion omelette — ₮26,000\n3 eggs, herbs, fresh greens",
            "bf_hot_pancakes": "Butter pancakes — ₮28,000\nFluffy pancakes, Mongolian butter, maple syrup",
            "bf_hot_toast": "Ham & cheese toast — ₮30,000\nBrioche bread, melted cheese, smoked ham",
            "bf_hot_benedict": "Eggs Benedict — ₮32,000\nPoached eggs, hollandaise sauce, ham, focaccia",

            "dn_starters_bansh": "Lamb dumplings in broth (Bansh) — ₮28,000\nHomemade dumplings, lamb, light soup",
            "dn_starters_beetroot": "Goat cheese with roasted beetroot — ₮32,000\nSweet, creamy, crunchy",
            "dn_starters_bisque": "Prawn bisque — ₮34,000\nRich seafood soup with cream",
            "dn_starters_burrata": "Burrata & tomatoes — ₮38,000\nFresh cheese, tomatoes, balsamic",

            "dn_mains_tsui_van": "Tsui Van (Mongolian noodles) — ₮34,000\nHand cut noodles, beef, vegetables",
            "dn_mains_lamb_pastry": "Crispy lamb pastry – Signature — ₮42,000\nInspired by khuushuur, with spicy sauce",
            "dn_mains_pizza": "Khanagar pizza – Signature — ₮45,000\nBeef, mushrooms, onion, cheese, wood-fired",
            "dn_mains_kungpao": "Kung Pao chicken — ₮52,000\nChicken, peanuts, chili, rice",
            "dn_mains_tortellini": "Pumpkin tortellini — ₮62,000\nPasta with creamy cheese sauce",
            "dn_mains_chicken": "Roasted chicken thigh — ₮68,000\nWith mushroom sauce and mashed potato",
            "dn_mains_fish": "Seared fish — ₮78,000\nWith butter sauce, spinach, capers",
            "dn_mains_short_rib": "Braised beef short rib — ₮85,000\nSlow cooked, very soft",
            "dn_mains_steak": "Grass-fed sirloin steak — ₮89,000\nWith mash and greens",
            "dn_mains_lamb_shoulder": "Braised lamb shoulder (Korean style) — ₮92,000\nSweet and spicy, with rice",

            "dn_desserts_icecream": "Camel milk ice cream — ₮24,000\nLight and slightly sweet",
            "dn_desserts_creme": "Goat milk crème brûlée — ₮26,000\nCreamy with caramel top",
            "dn_desserts_cheesecake": "Khanagar cheesecake — ₮28,000\nMade with camel milk cream cheese",

            "dr_cocktails_khan": "THE KHAN — ₮38,000\nWild Turkey bourbon, smoked honey, aged bitters, orange zest",
            "dr_cocktails_silkroad": "SILK ROAD — ₮38,000\nHendrick's gin, elderflower liqueur, fresh cucumber, rose water",

            "dr_wine_glass_sauvignon": "Fanagoria Sauvignon Blanc (150ml) — ₮30,000",
            "dr_wine_glass_chardonnay": "Fanagoria Chardonnay (150ml) — ₮34,000",
            "dr_wine_glass_cabernet": "Fanagoria Cabernet Sauvignon (150ml) — ₮32,000",
            "dr_wine_glass_merlot": "Fanagoria Merlot (150ml) — ₮34,000",
            "dr_wine_glass_rose": "Fanagoria Rosé (150ml) — ₮30,000",

            "dr_wine_bottle_sauvignon": "Fanagoria Sauvignon Blanc — ₮150,000 (750ml)",
            "dr_wine_bottle_chardonnay": "Fanagoria Chardonnay — ₮165,000 (750ml)",
            "dr_wine_bottle_cabernet": "Fanagoria Cabernet Sauvignon — ₮160,000 (750ml)",
            "dr_wine_bottle_merlot": "Fanagoria Merlot — ₮165,000 (750ml)",
            "dr_wine_bottle_brut": "Fanagoria Cru Lermont Brut — ₮185,000 (750ml)",

            "dr_spirits_glenmorangie": "Glenmorangie Original 10 Year (50ml) — ₮42,000",
            "dr_spirits_johnnie": "Johnnie Walker Black Label (50ml) — ₮38,000",
            "dr_spirits_jack": "Jack Daniel's Old No. 7 (50ml) — ₮35,000",
            "dr_spirits_hennessy": "Hennessy VS (50ml) — ₮45,000",

            "dr_soft_coke": "Coca-Cola — ₮8,000",
            "dr_soft_coke_zero": "Coca-Cola Zero — ₮8,000",
            "dr_soft_sprite": "Sprite — ₮8,000",
            "dr_soft_fanta": "Fanta Orange — ₮8,000",
            "dr_soft_sengur": "Sengur Premium Lager (500ml) — ₮15,000",
            "dr_soft_heineken": "Heineken (500ml) — ₮20,000",
            "dr_soft_orange": "Fresh Orange Juice — ₮12,000"
        }

        selected_item = item_info.get(item_full_key, "Selected item not found")
        item_name = selected_item.split(" — ")[0] if " — " in selected_item else selected_item

        text = f"**{item_name}**\n\n" \
               "Your order has been received! 🎉\n" \
               "Our team will prepare it shortly.\n" \
               "Thank you for choosing KHANAGAR 🌄"

        await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        await callback.answer("Order received! ✅")
        return

    await callback.message.edit_text("Section not implemented yet.")
    await callback.answer()


# Webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    try:
        update_json = await request.json()
        update = Update.de_json(update_json, bot)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Startup-д
@app.on_event("startup")
async def on_startup():
    webhook_url = "https://khanagar-bot.onrender.com/webhook"  
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    logger.info(f"Webhook set to: {webhook_url}")

async def main():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
