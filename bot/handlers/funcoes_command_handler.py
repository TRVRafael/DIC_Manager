from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from data import db_controller
from config import bot_logger

from bot.utils import get_fancy_name

funcoes_disponiveis = {
    1: 'auxiliar',
    2: 'sublider',
    3: 'vicelider',
    4: 'lider',
}

permission_slug_list = {
    'permissao_1': 'can_change_info',
    'permissao_2': 'can_delete_messages',
    'permissao_3': 'can_invite_users',
    'permissao_4': 'can_restrict_members',
    'permissao_5': 'can_pin_messages',
    'permissao_6': 'can_promote_members',
}

permission_labels = {
    'can_change_info': 'Alterar informações',
    'can_delete_messages': 'Excluir mensagens',
    'can_invite_users': 'Convidar usuários',
    'can_restrict_members': 'Restringir membros',
    'can_pin_messages': 'Fixar mensagens',
    'can_promote_members': 'Promover membros',
}

def get_role_permissions_from_db(role_name):
    current_role = funcoes_disponiveis[int(role_name.split('_')[1])]
    permissions = db_controller.get_role_permissions(current_role)
    if permissions is None:
        bot_logger.warning(f"Permissions for role '{current_role}' not found.")
        return {}
    
    return permissions

async def log(update: Update, context: CallbackContext):
    await db_controller.log_roles_with_permissions()

async def mudar_permissao(update: Update, context: CallbackContext, permissao: str):
    current_role = context.user_data.get('selected_role', None)

    for key, role in funcoes_disponiveis.items():
        if role == current_role:
            role_key = f'editar_{key}'
            break

    permissions = get_role_permissions_from_db(role_key)
    permission_slug = permission_slug_list[permissao]
    permissions[permission_slug] = not permissions[permission_slug]

    db_controller.update_role_permission(current_role, permission_slug, permissions[permission_slug])

    keyboard = [
        [InlineKeyboardButton(f"Alterar informações {'✅' if permissions[permission_slug_list['permissao_1']] else '❌'}", callback_data=f'permissao_1')],
        [InlineKeyboardButton(f"Excluir mensagens {'✅' if permissions[permission_slug_list['permissao_2']] else '❌'}", callback_data=f'permissao_2')],
        [InlineKeyboardButton(f"Convidar usuários {'✅' if permissions[permission_slug_list['permissao_3']] else '❌'}", callback_data=f'permissao_3')],
        [InlineKeyboardButton(f"Restringir membros {'✅' if permissions[permission_slug_list['permissao_4']] else '❌'}", callback_data=f'permissao_4')],
        [InlineKeyboardButton(f"Fixar mensagens {'✅' if permissions[permission_slug_list['permissao_5']] else '❌'}", callback_data=f'permissao_5')],
        [InlineKeyboardButton(f"Promover membros {'✅' if permissions[permission_slug_list['permissao_6']] else '❌'}", callback_data=f'permissao_6')],
        [InlineKeyboardButton("Voltar", callback_data='editar_permissoes'), InlineKeyboardButton("Finalizar", callback_data='finalizar')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if 'last_reply_markup' not in context.user_data or context.user_data['last_reply_markup'] != str(reply_markup):
        await update.callback_query.answer()
        await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        
        context.user_data['last_reply_markup'] = str(reply_markup)
    else:
        await update.callback_query.answer()

async def editar_permissoes(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f"{get_fancy_name(funcao)}", callback_data=f'editar_{numero}')] for numero, funcao in funcoes_disponiveis.items()
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Escolha a função para editar as permissões:", reply_markup=reply_markup)

async def finalizar(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Alterações concluídas!")

async def exibir_permissoes_funcao(update: Update, context: CallbackContext, role_name: str):
    # Get the permissions from the database
    permissions = get_role_permissions_from_db(role_name)

    # Create the keyboard dynamically based on the permissions
    keyboard = [
        [InlineKeyboardButton(f"{label} {'✅' if permissions.get(key) else '❌'}", callback_data=f'permissao_{i}')]
        for i, (key, label) in enumerate(permission_labels.items(), 1)
    ]
    
    # Add the Voltar and Finalizar buttons
    keyboard.append([InlineKeyboardButton("Voltar", callback_data='editar_permissoes'), 
                     InlineKeyboardButton("Finalizar", callback_data='finalizar')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Get the current role based on role_name
    current_role = funcoes_disponiveis[int(role_name.split('_')[1])]
    context.user_data['selected_role'] = current_role

    # Send the message with the permission buttons
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Editando permissões para: {get_fancy_name(current_role)}", reply_markup=reply_markup)

async def funcoes(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Editar permissões", callback_data='editar_permissoes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)
