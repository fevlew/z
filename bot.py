import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== ТОКЕН ==========
BOT_TOKEN = "8260065498:AAHvb8-APP8l5qE4c530Rh-0ka81EybOpso"

# ========== НАСТРОЙКИ ==========
IMAGE_SKINS = "skins.jpg"
IMAGE_GOLD = "gold.jpg"
IMAGE_PROMO = "promo.jpg"

# Ссылка на поддержку (ЗАМЕНИ НА СВОЮ!)
SUPPORT_LINK = "https://t.me/lelolamaa

# Реквизиты для оплаты
PAYMENT_DETAILS = (
    "💳 Номер карты: 2200 7013 8881 4953\n"
    "👤 Получатель: Антон К.\n"
    "💰 Банк: Тинькофф (Т-Банк)\n"
    "📱 После оплаты пришлите скрин сюда, мы проверим в течение 10 минут."
)

def get_rarities(count: int) -> str:
    rarities = ["Обычный", "Редкий", "Эпический", "Легендарный"]
    parts = [random.randint(0, count) for _ in range(3)]
    parts.sort()
    counts = [
        parts[0],
        parts[1] - parts[0],
        parts[2] - parts[1],
        count - parts[2]
    ]
    random.shuffle(counts)
    result = []
    for r, c in zip(rarities, counts):
        if c > 0:
            result.append(f"{r}: {c}")
    return ", ".join(result)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    keyboard = [
        [
            InlineKeyboardButton("🔫 Скины", callback_data="skins"),
            InlineKeyboardButton("🎫 Промокоды", callback_data="promo"),
            InlineKeyboardButton("💰 Голда", callback_data="gold"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="👇 Выбери раздел:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat.id

    # ===== РАЗДЕЛ СКИНЫ =====
    if data == "skins":
        try:
            with open(IMAGE_SKINS, 'rb') as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f
                )
        except:
            pass

        keyboard = [
            [InlineKeyboardButton("📦 Маленький пак (5 скинов) - 155₽", callback_data="skin_small")],
            [InlineKeyboardButton("📦 Средний пак (15 скинов) - 395₽", callback_data="skin_medium")],
            [InlineKeyboardButton("📦 Большой VIP пак (45 скинов) - 670₽", callback_data="skin_large")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Выбери пак:",
            reply_markup=reply_markup
        )

    # ===== РАЗДЕЛ ПРОМОКОДЫ =====
    elif data == "promo":
        try:
            with open(IMAGE_PROMO, 'rb') as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption="⏳ временно не работает, попробуйте позже."
                )
        except:
            await context.bot.send_message(
                chat_id=chat_id,
                text="⏳ временно не работает, попробуйте позже."
            )

    # ===== РАЗДЕЛ ГОЛДА =====
    elif data == "gold":
        try:
            with open(IMAGE_GOLD, 'rb') as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f
                )
        except:
            pass

        keyboard = [
            [InlineKeyboardButton("💎 Мини 100G - 80₽", callback_data="gold_small")],
            [InlineKeyboardButton("💎 Средний 250G - 190₽", callback_data="gold_medium")],
            [InlineKeyboardButton("💎 Мега пак (РЕКОМЕНДОВАНО) 500G - 350₽", callback_data="gold_large")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Выбери пак:",
            reply_markup=reply_markup
        )

    # ===== ПАКЕТЫ СКИНОВ =====
    elif data == "skin_small":
        text = ("🛍 *Маленький пак (5 скинов)*\n"
                "Цена: 155 рублей\n\n"
                f"🎲 Редкости: {get_rarities(5)}\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_skin_small")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "skin_medium":
        text = ("🛍 *Средний пак (15 скинов)*\n"
                "Цена: 395 рублей\n\n"
                f"🎲 Редкости: {get_rarities(15)}\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_skin_medium")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "skin_large":
        text = ("🛍 *Большой VIP пак (45 скинов)*\n"
                "Цена: 670 рублей\n\n"
                f"🎲 Редкости: {get_rarities(45)}\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_skin_large")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    # ===== ПАКЕТЫ ГОЛДЫ =====
    elif data == "gold_small":
        text = ("💎 *Мини 100G*\n"
                "Цена: 80 рублей\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_gold_small")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "gold_medium":
        text = ("💎 *Средний 250G*\n"
                "Цена: 190 рублей\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_gold_medium")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "gold_large":
        text = ("💎 *Мега пак 500G* (РЕКОМЕНДОВАНО)\n"
                "Цена: 350 рублей\n\n"
                "👇 Для оплаты нажми кнопку ниже.")
        keyboard = [[InlineKeyboardButton("💳 Оплатить", callback_data="pay_gold_large")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    # ===== ОПЛАТА =====
    elif data.startswith("pay_"):
        # КНОПКА ПОДДЕРЖКИ + реквизиты
        keyboard = [
            [InlineKeyboardButton("🆘 Обратиться в поддержку", url=SUPPORT_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=("🧾 *Оплата*\n\n"
                  f"{PAYMENT_DETAILS}\n\n"
                  "🕐 Ожидаем подтверждения. Проверим в течение 10 минут и свяжемся с вами."),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()