from telegram import Update
from telegram.ext import CallbackContext

from data import db_controller
from config import bot_logger

def message_is_on_group(chatId: float) -> bool:
    all_chats = db_controller.get_all_chats()
    official_chats = [chat for chat in all_chats if chat[2] == 1]

    for chat in official_chats:
        if float(chat[0]) == chatId and chat[2] == 1:
            return True
    return False

async def user_is_group_admin(update : Update) -> bool:
    """Verifica se um usuário é administrador do chat.

    Args:
        update (Update): Objeto de Update do pacote 'telegram'.

    Returns:
        bool: True se o usuário for admin, False caso contrário.
    """
    chat_admins_list = await update.effective_chat.get_administrators()
    return update.effective_user in (admin.user for admin in chat_admins_list)

async def oficializar(update : Update, context: CallbackContext):
    CHAT_ID = update.effective_chat.id
    current_chat = db_controller.get_chat_by_id(str(CHAT_ID))
    is_chat_official = current_chat[2]

    if is_chat_official == 0:
        db_controller.set_chat_as_official(str(CHAT_ID))
        await update.message.reply_text(f"⭐ <b>Chat {current_chat[1]} definido como oficial.</b>", parse_mode="HTML")
        bot_logger.info(f"Chat {current_chat[1]} : {current_chat[0]} definido como oficial. > Responsável: @{update.effective_user.username}")
    else:
        await update.message.reply_text(f"<b>Esse chat já é oficial.</b>\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        
async def kick(update: Update, context: CallbackContext):
    CHAT_ID = update.effective_chat.id
    message = update.message

    if not message_is_on_group(CHAT_ID):
        await message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário @{update.effective_user.username} tentou utilizar o comando /cargo fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return
    
    if not await user_is_group_admin(update):
        await message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou, sem permissão, o comando /kick | Chat: {format_chat_object(update)}")
        return
    
    username = context.args[0]

    try:
        if username.startswith('@'):
            username = username[1:]

        user_id = db_controller.get_user_id_by_username(username)

        await message.chat.ban_member(user_id)

        await message.reply_text(f"<b>✅ Usuário @{username} foi expulso do grupo.</b>", parse_mode="HTML")
        bot_logger.info(f"Usuário {username} foi expulso do grupo. > Responsável: {update.effective_user.username}")
    except Exception as err:
        await message.reply_text(f"<b>✅ Algum erro ocorreu durante a execução do comando, contate a equipe de desenvolvedores.</b>", parse_mode="HTML")
        bot_logger.info(f"Erro ao remover usuário do grupo: {err}")
