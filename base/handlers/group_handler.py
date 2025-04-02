from telegram import Update, Bot
from telegram.ext import CallbackContext
import time

from data import db_controller
from config import bot_logger
from base.shared_modules import not_chat_admin_handler, not_official_chat_handler, not_at_char_handler

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
    from base.handlers import update_members_message
    CHAT_ID = update.effective_chat.id
    message = update.message
    div_name = context.bot_data['div']

    if not message_is_on_group(CHAT_ID):
        await not_official_chat_handler(update)
        return
    
    if not await user_is_group_admin(update):
        await not_chat_admin_handler(update, "/kick")
        return
    
    username = context.args[0]
    
    user_data = db_controller.get_user_id_by_username(f"@{username[1:]}", div_name)
    if not user_data:
        await message.reply_text("❌ Usuário não encontrado no banco de dados")
        return
    user_id = user_data[0]
    
    try:
        if not username.startswith('@'):
            not_at_char_handler(update)
            return
        username = username[1:]
        
        bot = Bot(context.bot.token)
        div_name = context.bot_data['div']
        current_unix = int(time.time())

        # Timestamp daqui a 1 minuto (60 segundos)
        future_unix = current_unix + 60

        await bot.ban_chat_member(message.chat.id, user_id, until_date=future_unix)
        db_controller.delete_member(f"@{username}", div_name)
        await update_members_message(CHAT_ID, context)
        await message.reply_text(f"<b>✅ Usuário @{username} foi expulso do grupo.</b>", parse_mode="HTML")
        bot_logger.info(f"Usuário {username} foi expulso do grupo. > Responsável: {update.effective_user.username}")
    except Exception as err:
        await message.reply_text(f"<b>✅ Algum erro ocorreu durante a execução do comando, contate a equipe de desenvolvedores.</b>", parse_mode="HTML")
        bot_logger.info(f"Erro ao remover usuário do grupo: {err}")
