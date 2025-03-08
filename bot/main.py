from telegram.ext import CommandHandler, Application, MessageHandler, filters

from bot.config import BOT_TOKEN
from bot.handlers import apelidar, handle_new_user
from config.logging_config import setup_logging


# Configuração do logging
setup_logging()
        

def start_bot() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("set", apelidar))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
    
    print("Bot rodando...")
    app.run_polling()
    