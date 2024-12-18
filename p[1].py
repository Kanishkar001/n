import telebot
import os
import threading
from datetime import datetime

API_TOKEN = '7489424546:AAGEBRysBgHW1qH214LMR5hthH9iObkxYVA'  # Replace with your bot's API token
AUTHORIZED_USER_ID = 1787949670  # Replace with your Telegram user ID

bot = telebot.TeleBot(API_TOKEN)

# Command execution history
command_history = []

# Import the original functionality
from script2 import (
    handle_selection,
    display_menu,
    clear_screen
)

# Telegram-based menu handler
@bot.message_handler(commands=["start"])
def start_command(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(
            message.chat.id,
            (
                "👋 Welcome to the Vulnerability Scanner Bot!\n\n"
                "📜 Available options:\n"
                "1️⃣ LFI Scanner\n"
                "2️⃣ OR Scanner\n"
                "3️⃣ SQLi Scanner\n"
                "4️⃣ XSS Scanner\n"
                "5️⃣ Update Tool\n"
                "6️⃣ Exit\n\n"
                "ℹ️ Send the corresponding number (1-6) to select an option."
            )
        )
    else:
        bot.send_message(message.chat.id, "❌ Unauthorized access.")

# Handle menu selections
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_selection_command(message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "❌ Unauthorized access.")
        return

    selection = message.text.strip()
    if selection in ["1", "2", "3", "4", "5", "6"]:
        bot.send_message(message.chat.id, f"Processing option {selection}...")
        threading.Thread(target=execute_option, args=(message.chat.id, selection)).start()
    else:
        bot.send_message(message.chat.id, "❓ Invalid selection. Please send a number between 1 and 6.")

# Execute the selected option
def execute_option(chat_id, selection):
    try:
        clear_screen()  # Ensure terminal clears for better execution
        handle_selection(selection)  # Call the existing function
        bot.send_message(chat_id, f"✅ Option {selection} executed successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error executing option {selection}: {e}")

# Fallback handler for unknown commands
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_message(
        message.chat.id,
        "❓ Unknown command. Use /start to view available options."
    )

# Start polling
bot.polling()