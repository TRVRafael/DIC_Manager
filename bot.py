from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Application, ChatMemberHandler, MessageHandler, filters

from db_controller import Database
from auth.bot_config import BOT_TOKEN

TOKEN = BOT_TOKEN
db_controller = Database()

async def give_admin_and_change_name(update: Update, context: CallbackContext) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        CHAT_ID = update.effective_chat.id
        
        bot = context.bot
        
        if len(context.args) < 2:
            await update.message.reply_text("Uso correto: /set @usuario nickname")
            return
        
        username = context.args[0]
        custom_title = " ".join(context.args[1:])
        
        username = context.args[0]
    
        if not username.startswith("@"):
            await update.message.reply_text("Por favor, mencione o usuário com @.")
            return
        
        user_id = db_controller.get_user_id_by_username(username=username[1:])
        
        if not user_id:
            await update.message.reply_text("O usuário especificado não existe.")

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

    else:
        await update.message.reply_text("Você não possui permissão.")
        

async def handle_new_user(update : Update, context : CallbackContext) -> None:
    for new_member in update.message.new_chat_members:
        db_controller.create_new_user(new_member.id, new_member.username)
        

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("set", give_admin_and_change_name))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_user))
    
    print("Bot rodando...")
    app.run_polling()
    

if __name__ == "__main__":
    main()