#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from datetime import date, datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "7886674539:AAGsIw5C5AHNOtGM8l2-NRqc7L4QZuPVZZw"
PERIOD = 1  # Initial period number

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me Bcone price to get prediction.",
    )

def get_sum(n):
    return sum(int(digit) for digit in str(n))

async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle received price and send prediction."""
    global PERIOD
    try:
        current = int(update.message.text)
        last_two = str(current)[-2:]
        
        # Calculate prediction
        if PERIOD % 2 == 0:
            total = get_sum(current)
            prediction = "🔴 RED" if total % 2 == 0 else "🟢 GREEN"
        else:
            total = get_sum(current)
            prediction = "🔴 RED" if total % 2 == 0 else "🟢 GREEN"
        
        response = f"Period {PERIOD+1} Prediction: {prediction}"
        PERIOD += 1
        
        await update.message.reply_text(response)
        
    except ValueError:
        await update.message.reply_text("Please send a valid integer price.")

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
