from telegram.ext import CommandHandler, Application, MessageHandler, filters

from bot.config import BOT_TOKEN
from bot.handlers import apelidar, handle_new_user, cargo, handle_user_removed, oficializar, force_control_message_update, kick
from config.logging_config import setup_logging

setup_logging()        

def start_bot() -> None:
    """
    Ponto de execução principal do bot.
    """
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("apelidar", apelidar))
    app.add_handler(CommandHandler("cargo", cargo))
    app.add_handler(CommandHandler("oficializar", oficializar))
    app.add_handler(CommandHandler("teste", teste))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("force_update", force_control_message_update))
    app.add_handler(CommandHandler("kick", kick))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_user_removed))
    
    print("Bot rodando...")
    app.run_polling()