import logging

from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import user_is_group_admin, format_chat_object
from data.database import Database


# Configuração do controlador da base de dados
db_controller = Database()


async def handle_new_user(update : Update, context : CallbackContext) -> None:
    """
    Armazena um novo usuário na base de dados.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
    
    """
    for new_member in update.message.new_chat_members:
        db_controller.create_new_user(new_member.id, new_member.username)
        

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
    
