from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import format_chat_object
from bot.handlers import message_is_on_group, user_is_group_admin
from config import bot_logger
from data import db_controller

async def verificar(update: Update, context: CallbackContext) -> None:
    """
    Dá o administrador com nome personalizado ao usuário especificado.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.

    """
    CHAT_ID = update.effective_chat.id

    if not message_is_on_group(CHAT_ID):
        await update.message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário {update.effective_user.username} tentou utilizar o comando /verificar fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return

    if not await user_is_group_admin(update):
        await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou, sem permissão, o comando /verificar | Chat: {format_chat_object(update)}")
        return
        
    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /verificar @usuario nickname")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou o comando /verificar sem todos argumentos ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    username = context.args[0]
    custom_title = " ".join(context.args[1:])
        
    username = context.args[0]
    
    if not username.startswith("@"):
        await update.message.reply_text("Por favor, mencione o usuário com @.")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou o comando /verificar sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    user_id = db_controller.get_user_id_by_username(username=username[1:])
        
    if not user_id:
        await update.message.reply_text("O usuário especificado não existe. (Tratar erro: nome passado errado ou nome correto, mas bot não reconheceu.)")
    
    
    # Waiting for the complete procedure definition

    # await bot.promote_chat_member(
    #     chat_id=CHAT_ID,
    #     user_id=user_id,
    #     can_change_info=True,
    #     can_delete_messages=False,
    #     can_invite_users=False,
    #     can_restrict_members=False,
    #     can_pin_messages=False,
    #     can_promote_members=False
    # )

    # await bot.set_chat_administrator_custom_title(
    #     chat_id=CHAT_ID,
    #     user_id=user_id,
    #     custom_title=custom_title
    # )
    
    db_controller.insert_member_in_division(user_id, username, custom_title)
    await update.message.reply_text(f"✏️ Apelido <b>{custom_title}</b> atribuido ao usuário <b>{username}</b>.", parse_mode="HTML")
    bot_logger.info(f"Apelido {custom_title} atribuido ao usuário {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")  

async def remover_apelido(update: Update, context: CallbackContext) -> None:
    """
    Remove o administrador com nome personalizado do usuário especificado.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.

    """
    CHAT_ID = update.effective_chat.id

    if not message_is_on_group(CHAT_ID):
        await update.message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário {update.effective_user.username} tentou utilizar o comando /remover_apelido fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return

    if not await user_is_group_admin(update):
        await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou, sem permissão, o comando /remover_apelido | Chat: {format_chat_object(update)}")
        return
        
    if len(context.args) < 1:
        await update.message.reply_text("Uso correto: /remover_apelido @usuario")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou o comando /remover_apelido sem todos argumentos ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    username = context.args[0]
        
    if not username.startswith("@"):
        await update.message.reply_text("Por favor, mencione o usuário com @.")
        bot_logger.info(f"Usuário {update.effective_user.username} utilizou o comando /remover_apelido sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    user_id = db_controller.get_user_id_by_username(username=username[1:])
        
    if not user_id:
        await update.message.reply_text("O usuário especificado não existe. (Tratar erro: nome passado errado ou nome correto, mas bot não reconheceu.)")
        bot_logger.info(f"Usuário {update.effective_user.username} tentou remover apelido de um usuário inexistente ({update.message.text}) | Chat: {format_chat_object(update)}")
        return

    # Remove the custom title from the user
    await context.bot.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=user_id,
        can_change_info=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False
    )

    await context.bot.set_chat_administrator_custom_title(
        chat_id=CHAT_ID,
        user_id=user_id,
        custom_title=""
    )

    db_controller.remove_member_from_division(user_id)
    await update.message.reply_text(f"✏️ Apelido removido do usuário <b>{username}</b>.", parse_mode="HTML")
    bot_logger.info(f"Apelido removido do usuário {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")