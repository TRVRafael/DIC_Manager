from telegram import Update


async def user_is_group_admin(update : Update) -> bool:
    """Verifica se um usuário é administrador do chat.

    Args:
        update (Update): Objeto de Update do pacote 'telegram'.

    Returns:
        bool: True se o usuário for admin, False caso contrário.
    """
    chat_admins_list = await update.effective_chat.get_administrators()
    return update.effective_user in (admin.user for admin in chat_admins_list)


def format_chat_object(update : Update) -> str:
    """Formata as informações do chat de um Update.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        
    Returns:
        str: chat_title (chat_id)
    """
    return f"{update.effective_chat.title} ({update.effective_chat.id})"


def sanitize_role_name(role_name_input : str) -> str:
    """Format a given role name to the correct format.
    
    Args:
        role_name_input (str): Role name given by the user.
        
    Returns:
        str: Role name in the correct format.
    """
    return role_name_input.replace("-", "").replace("í","i").lower()

