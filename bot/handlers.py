import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler

from bot.utils import user_is_group_admin, format_chat_object
from data.database import Database

# Configuração do controlador da base de dados
db_controller = Database()


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
                logging.info(f"Bot adicionado ao chat: {chat_title} - {chat_id}")

            chat_data = db_controller.get_all_chats()
            logging.info(f"Lista de chats do bot atualizada: {chat_data}")
        else:
            db_controller.create_new_user(new_member.id, new_member.username)

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
        logging.info(f"Bot removido do chat: {chat_title} - {chat_id}")

        chat_data = db_controller.get_all_chats()
        logging.info(f"Lista de chats do bot atualizada: {chat_data}")

async def apelidar(update: Update, context: CallbackContext) -> None:
    """
    Dá o administrador com nome personalizado ao usuário especificado.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.

    """
    if not await user_is_group_admin(update):
        await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"Usuário {update.effective_user.username} utilizou, sem permissão, o comando /apelidar | Chat: {format_chat_object(update)}")
        return
        
    CHAT_ID = update.effective_chat.id
        
    bot = context.bot
        
    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /set @usuario nickname")
        logging.info(f"Usuário {update.effective_user.username} utilizou o comando /apelidar sem todos argumentos ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    username = context.args[0]
    custom_title = " ".join(context.args[1:])
        
    username = context.args[0]
    
    if not username.startswith("@"):
        await update.message.reply_text("Por favor, mencione o usuário com @.")
        logging.info(f"Usuário {update.effective_user.username} utilizou o comando /apelidar sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    user_id = db_controller.get_user_id_by_username(username=username[1:])
        
    if not user_id:
        await update.message.reply_text("O usuário especificado não existe. (Tratar erro: nome passado errado ou nome correto, mas bot não reconheceu.)")

    await bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user_id,
        can_change_info=True,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False
    )

    await bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=user_id,
        custom_title=custom_title
    )
    
    await update.message.reply_text(f"✏️ Apelido <b>{custom_title}</b> atribuido ao usuário <b>{username}</b>.", parse_mode="HTML")
    logging.info(f"Apelido {custom_title} atribuido ao usuário {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")
    

async def cargo(update : Update, context : CallbackContext):
    
    CHAT_ID = update.effective_chat.id
    username = context.args[0]
    role_name = " ".join(context.args[1:])
    
    bot = context.bot
    
    if not username.startswith("@"):
        await update.message.reply_text("Por favor, mencione o usuário com @.")
        logging.info(f"Usuário {update.effective_user.username} utilizou o comando /apelidar sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    user_id = db_controller.get_user_id_by_username(username=username[1:])
        
    if not user_id:
        await update.message.reply_text("O usuário especificado não existe. (Tratar erro: nome passado errado ou nome correto, mas bot não reconheceu.)")

    role_permissions = db_controller.get_role_permissions(role_name)
    
    await bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user_id,
        can_change_info=role_permissions['can_change_info'],
        can_delete_messages=role_permissions['can_delete_messages'],
        can_invite_users=role_permissions['can_invite_users'],
        can_restrict_members=role_permissions['can_restrict_members'],
        can_pin_messages=role_permissions['can_pin_messages'],
        can_promote_members=role_permissions['can_promote_members']
    )

    await bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=user_id,
        custom_title=role_name
    )
