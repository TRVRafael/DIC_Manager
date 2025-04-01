from telegram.ext import CommandHandler, Application, MessageHandler, CallbackQueryHandler, filters

from bot.config import BOT_TOKEN
from bot.handlers import verificar, apelidar, handle_new_user, handle_user_removed, oficializar, force_members_message_update, kick, remover_apelido
from bot.handlers.list_command_handler import log_role, log_lideres

roles = {
    "membros": 0,
    "auxiliares": 1,
    "core": 5,
    "comando": 6,
    "comandogeral": 7,
    "presidencia": 8,
}
from bot.handlers.funcoes_command_handler import editar_permissoes, mudar_permissao, funcoes, exibir_permissoes_funcao, finalizar

from data import db_controller

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

    app.add_handler(CommandHandler("funcoes", funcoes))
    app.add_handler(CallbackQueryHandler(editar_permissoes, pattern='^editar_permissoes$'))
    app.add_handler(CallbackQueryHandler(finalizar, pattern='^finalizar$'))
    
    for i in range(1, 7):
        app.add_handler(CallbackQueryHandler(
            lambda update, context, i=i: exibir_permissoes_funcao(update, context, f'editar_{i}'),
            pattern=f'^editar_{i}$'
        ))

    for i in range(1, 7):
        app.add_handler(CallbackQueryHandler(
            lambda update, context, i=i: mudar_permissao(update, context, f'permissao_{i}'),
            pattern=f'^permissao_{i}$'
        ))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_user_removed))
    
    print("Bot rodando...")
    app.run_polling()