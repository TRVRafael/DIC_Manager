import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
from database import Database

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

db = Database()
db._init_user_table()

async def novo_membro(update: Update, context):
    """Função chamada quando novos membros entram no grupo
    Registra os novos usuários no banco de dados"""
    novos_membros = update.message.new_chat_members
    
    for membro in novos_membros:
        user_id = membro.id
        username = membro.username if membro.username else "Sem username"
        nome = membro.full_name

        db.create_new_user(user_id, username)
        logging.info(f"Novo membro adicionado: {nome} (@{username})")

async def ver_membros(update: Update, context: CallbackContext) -> None:
    """Comando que retorna a lista de usuários cadastrados no banco"""
    membros = db.get_all_users()

    if not membros:
        mensagemFormatada = "Nenhum usuário adicionado ainda"
    else:
        mensagemFormatada = "\n".join(
            [f"🔹 ID: {m['user_id']} - {m['username']}" for m in membros]
        )
    print("📋 Dados dos Membros:")
    db.get_all_users()

    await update.message.reply_text(f"📋 Dados dos Membros:\n{mensagemFormatada}")

def main():
    """Função principal que inicializa o bot e adiciona os handlers"""
    TOKEN = "token aquii"

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, novo_membro))
    app.add_handler(CommandHandler("verDados", ver_membros))
    
    logging.info("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()