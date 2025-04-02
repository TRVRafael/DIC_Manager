from telegram import Update, error
from telegram.ext import CallbackContext

from config import bot_logger

from data import db_controller
from base.handlers import message_is_on_group, user_is_group_admin, update_members_message
from base.shared_modules import (
    not_official_chat_handler,
    not_chat_admin_handler,
    not_at_char_handler,
    error_default_handler,
    format_chat_object, 
    sanitize_role_name, 
    get_fancy_name
)




async def apelidar(update : Update, context : CallbackContext):
    CHAT_ID = update.effective_chat.id
    div_name = context.bot_data['div']
    
    if not message_is_on_group(CHAT_ID):
        await not_official_chat_handler(update)
        return

    # Adicionando a checagem de admin da versão "main"
    if not await user_is_group_admin(update):
        await not_chat_admin_handler(update, "/apelidar")
        return
    
    username = context.args[0]
    role_name_input = " ".join(context.args[1:])
    role_name = sanitize_role_name(role_name_input)

    bot = context.bot
    
    if not username.startswith("@"):
        await not_at_char_handler(update)
        return
        
    (user_id, nickname_from_db) = db_controller.get_user_id_by_username(f"@{username[1:]}", div_name)
     
    role_permissions = db_controller.get_role_permissions(role_name, div_name)
    
    
    if not nickname_from_db:
        await error_default_handler("Utilize o comando /verificar antes de atribuir o apelido.", update=update)
        return
    elif not user_id:
        await error_default_handler("A conta informada não existe no chat.", update=update)
        return
    elif not role_permissions:
        await error_default_handler("O cargo informado é inválido.", update=update)
        return

    try:
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
            custom_title=get_fancy_name(role_name)
        )
        
        db_controller.update_member_role(username, db_controller.get_role_id(role_name, div_name), div_name)
        await update_members_message(update.effective_chat.id, context)
        
        await update.message.reply_text(f"<b>✅ Cargo {role_name} atribuido ao usuário {username} com sucesso.</b>", parse_mode="HTML")
        bot_logger.info(f"Cargo {role_name} atribuído a {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")
        
    except error.BadRequest as err:
        if "Not enough rights" in str(err):
            await update.message.reply_text(f"<b>❌ O Bot necessita ser administrador do grupo para esse comando.</b>", parse_mode="HTML")
            bot_logger.error(f"TELEGRAM ERROR: {err}")
            
    except Exception as err:
        await update.message.reply_text(f"<b>❌ Erro atribuindo cargo ao usuário {username}</b>\n<i>Contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        bot_logger.warning(f"Erro atribuindo cargo ao usuário {username} - ({update.message.text})| Chat: {format_chat_object(update)} -> {err}")
        

async def update_role_permissions_for_all_members(context: CallbackContext, role_name: str, div_name: str):
    """Atualiza permissões para todos os membros com um determinado cargo"""
    try:
        role_permissions = db_controller.get_role_permissions(role_name, div_name)
        
        if not role_permissions:
            bot_logger.error(f"Cargo {role_name} não encontrado para atualização em massa")
            return
        
        bot = context.bot

        roles_ids = {
            'membro': 0,
            'auxiliar': 1,
            'sublider': 2,
            'vicelider': 3,
            'lider': 4
        }
        members_with_role = db_controller.get_members_user_id_by_role(roles_ids[role_name], div_name)
        
        if not members_with_role:
            bot_logger.info(f"Nenhum membro com cargo {role_name} para atualizar")
            return

        # 3. Atualiza cada membro
        for member in members_with_role:
            username = member[0]
            user_id = member[1]
            
            try:
                await bot.promote_chat_member(
                    chat_id=context.bot_data['chat_id'],
                    user_id=user_id,
                    can_change_info=role_permissions['can_change_info'],
                    can_delete_messages=role_permissions['can_delete_messages'],
                    can_invite_users=role_permissions['can_invite_users'],
                    can_restrict_members=role_permissions['can_restrict_members'],
                    can_pin_messages=role_permissions['can_pin_messages'],
                    can_promote_members=role_permissions['can_promote_members']
                )
                
                await bot.set_chat_administrator_custom_title(
                    chat_id=context.bot_data['chat_id'],
                    user_id=user_id,
                    custom_title=get_fancy_name(role_name)
                )
                
                bot_logger.info(f"Permissões atualizadas para @{username[1:] if username.startswith('@') else username} ({role_name})")
                
            except Exception as e:
                bot_logger.error(f"Erro ao atualizar permissões para @{username[1:]}: {str(e)}")
                continue

    except Exception as e:
        bot_logger.critical(f"Falha na atualização em massa de permissões: {str(e)}")
