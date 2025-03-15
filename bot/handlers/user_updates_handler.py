from telegram import Update
from telegram.ext import CallbackContext

from data import db_controller
from config import bot_logger

async def handle_new_user(update : Update, context : CallbackContext) -> None:
    """
    Verifica se o novo usuário é ou não o próprio bot, se for, adiciona o chat na lista de chat, se não, adiciona um novo usuário na tabela de usuários.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.
    """
    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            chat = update.message.chat
            chat_id = chat.id
            chat_title = chat.title

            chat_data = db_controller.get_all_chats()

            if not any(existing_chat[0] == str(chat_id) for existing_chat in chat_data):
                db_controller.create_new_chat(str(chat_id), chat_title)
                bot_logger.info(f"Bot adicionado ao chat: {chat_title} - {chat_id}")

            chat_data = db_controller.get_all_chats()
            bot_logger.info(f"Lista de chats do bot atualizada: {chat_data}")
        else:
            db_controller.create_new_user(new_member.id, new_member.username)
            bot_logger.info(f"Novo usuário: {new_member.username}")

async def handle_user_removed(update: Update, context: CallbackContext) -> None:
    """
    Realiza a remoção do chat da lista de chats do bot quando ele é removido.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.
    """
    left_member = update.message.left_chat_member

    if left_member.id == context.bot.id:
        chat = update.message.chat
        chat_id = chat.id
        chat_title = chat.title

        db_controller.delete_chat_by_id(str(chat_id))
        bot_logger.info(f"Bot removido do chat: {chat_title} - {chat_id}")

        chat_data = db_controller.get_all_chats()
        bot_logger.info(f"Lista de chats do bot atualizada: {chat_data}")
    else:
        bot_logger.info(f"O usuário {left_member.username} : {left_member.id} saiu do grupo.")