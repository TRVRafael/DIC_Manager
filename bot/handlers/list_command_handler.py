from telegram import Update
from telegram.ext import CallbackContext

from data import db_controller

role_names = {
    1: "Membros",
    2: "Auxiliares",
    5: "CORE",
    6: "Comando",
    7: "Comando-Geral",
    8: "Presidência",
}

async def log_role(update : Update, context : CallbackContext, role_id : int):
    members = db_controller.get_members_by_role(role_id)
    role_name = role_names.get(role_id, "Lista")

    message_lines = [f"📋 <b>{role_name}:</b>\n"]

    if members:
        if len(members) > 0:
            for index, (telegram_handle, username) in enumerate(members, start=1):
                message_lines.append(f"{telegram_handle} - {username}")
        else:
            message_lines.append("Lista vazia.")
    else:
         message_lines.append("Lista vazia.")

    message_text = "\n".join(message_lines)
    await update.message.reply_text(message_text, parse_mode="HTML")

async def log_lideres(update: Update, context: CallbackContext):
    roles = {
        "🏅 <b>Sub-Líderes:</b>\n": 3,
        "👑 <b>Liderança</b>\n": 4,
    }

    message_lines = []
    
    for title, role_id in roles.items():
        members = db_controller.get_members_by_role(role_id)

        if members:
            message_lines.append(title)
            for telegram_handle, username in members:
                message_lines.append(f"{telegram_handle} - {username}")
            message_lines.append("") 

    message_text = "\n".join(message_lines) if message_lines else "Nenhum líder encontrado."
    
    await update.message.reply_text(message_text, parse_mode="HTML")

    