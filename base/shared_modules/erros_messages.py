from telegram import Update

from config import bot_logger
from base.shared_modules import format_chat_object

async def not_official_chat_handler(update: Update) -> None:
    await update.message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
    bot_logger.info(f"Usuário @{update.effective_user.username} tentou utilizar o comando /cargo fora de um grupo autorizado | Chat: {format_chat_object(update)}")
    return

async def not_chat_admin_handler(update: Update, command: str) -> None:
    await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
    bot_logger.info(f"Usuário @{update.effective_user.username} utilizou {command}, sem ser Administrador. | Chat: {format_chat_object(update)}")
    return

async def not_at_char_handler(update: Update) -> None:
    await update.message.reply_text("Por favor, mencione o usuário com @.")
    bot_logger.info(f"Usuário {update.effective_user.username} utilizou o comando /cargo sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
    return

async def error_default_handler(text: str, update: Update) -> None:
    await update.message.reply_text(f"❌ <b>{text}</b>", parse_mode="HTML")
    bot_logger.warning(f"{text} | Message: {update.effective_message.text} | Chat: {format_chat_object(update)}")