from telegram.ext import CommandHandler, Application, MessageHandler, filters

from bot.config import BOT_TOKEN
from bot.handlers import verificar, apelidar, handle_new_user, handle_user_removed, oficializar, force_members_message_update, kick, remover_apelido
from bot.handlers.list_command_handler import log_role, log_lideres

roles = {
    "membros": 1,
    "auxiliares": 2,
    "core": 5,
    "comando": 6,
    "comandogeral": 7,
    "presidencia": 8,
}

def start_bot() -> None:
    """
    Ponto de execução principal do bot.
    """
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("verificar", verificar))
    app.add_handler(CommandHandler("apelidar", apelidar))
    app.add_handler(CommandHandler("oficializar", oficializar))
    app.add_handler(CommandHandler("force_update", force_members_message_update))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("remover_apelido", remover_apelido))

    app.add_handler(CommandHandler("lideranca", log_lideres))
    for command, role_id in roles.items():
        app.add_handler(CommandHandler(command, lambda update, context, role_id=role_id: log_role(update, context, role_id)))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_user_removed))
    
    print("Bot rodando...")
    app.run_polling()