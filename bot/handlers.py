import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CallbackQueryHandler

from bot.utils import user_is_group_admin, format_chat_object, sanitize_role_name, get_fancy_name
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
    else:
        print(left_member.id)

async def apelidar(update: Update, context: CallbackContext) -> None:
    """
    Dá o administrador com nome personalizado ao usuário especificado.
    
    Args:
        update (Update): Objeto de Update do pacote 'telegram'.
        context (CallbackContext): Objeto de CallbackContext do pacote 'telegram'.

    """
    CHAT_ID = update.effective_chat.id

    if not message_is_on_group(CHAT_ID):
        await update.message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"Usuário {update.effective_user.username} tentou utilizar o comando /apelidar fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return

    if not await user_is_group_admin(update):
        await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"Usuário {update.effective_user.username} utilizou, sem permissão, o comando /apelidar | Chat: {format_chat_object(update)}")
        return
        
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
    logging.info(f"Apelido {custom_title} atribuido ao usuário {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")   

async def cargo(update : Update, context : CallbackContext):
    CHAT_ID = update.effective_chat.id
    if not message_is_on_group(CHAT_ID):
        await update.message.reply_text(f"Comandos só podem ser usados em grupos autorizados.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"Usuário @{update.effective_user.username} tentou utilizar o comando /cargo fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return

# Adicionando a checagem de admin da versão "main"
    if not await user_is_group_admin(update):
        await update.message.reply_text(f"Você não possui permissão para utilizar esse comando.\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"Usuário @{update.effective_user.username} utilizou, sem permissão, o comando /cargo | Chat: {format_chat_object(update)}")
        logging.info(f"Usuário {update.effective_user.username} tentou utilizar o comando /cargo fora de um grupo autorizado | Chat: {format_chat_object(update)}")
        return
    username = context.args[0]
    role_name_input = " ".join(context.args[1:])
    role_name = sanitize_role_name(role_name_input)

    bot = context.bot
    
    if not username.startswith("@"):
        await update.message.reply_text("Por favor, mencione o usuário com @.")
        logging.info(f"Usuário {update.effective_user.username} utilizou o comando /cargo sem @ no username ({update.message.text}) | Chat: {format_chat_object(update)}")
        return
        
    user_id = db_controller.get_user_id_by_username(username=username[1:])
        
    if not user_id:
        await update.message.reply_text("O usuário especificado não existe. (Tratar erro: nome passado errado ou nome correto, mas bot não reconheceu.)")

    role_permissions = db_controller.get_role_permissions(role_name)

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
        
        db_controller.update_member_role(username, db_controller.get_role_id(role_name))
        
        await update.message.reply_text(f"<b>✅ Cargo {role_name} atribuido ao usuário {username} com sucesso.</b>", parse_mode="HTML")
        logging.info(f"Cargo {role_name} atribuído a {username} > Responsável: @{update.effective_user.username} | Chat: {format_chat_object(update)}")
    except Exception as err:
        await update.message.reply_text(f"<b>❌ Cargo inserido é inválido. Tente novamente.</b>\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")
        logging.info(f"EXCEPTION: {err}")
        logging.info(f"@{update.effective_user.username} utilizou um nome de cargo inválido ({role_name_input} > {role_name})| Chat: {format_chat_object(update)}")

async def oficializar(update : Update, context: CallbackContext):
    CHAT_ID = update.effective_chat.id
    current_chat = db_controller.get_chat_by_id(str(CHAT_ID))
    is_chat_official = current_chat[2]

    if is_chat_official == 0:
        db_controller.set_chat_as_official(str(CHAT_ID))
        await update.message.reply_text(f"⭐ <b>Chat {current_chat[1]} definido como oficial.</b>", parse_mode="HTML")
        logging.info(f"Chat {current_chat[1]} : {current_chat[0]} definido como oficial. > Responsável: @{update.effective_user.username}")
    else:
        await update.message.reply_text(f"<b>Esse chat já é oficial.</b>\n\n<i>Caso isso seja um erro, contate a Equipe de Desenvolvedores, através da liderança da divisão.</i>", parse_mode="HTML")

def message_is_on_group(chatId: float) -> bool:
    all_chats = db_controller.get_all_chats()
    official_chats = [chat for chat in all_chats if chat[2] == 1]

    for chat in official_chats:
        if float(chat[0]) == chatId and chat[2] == 1:
            return True
    return False

def is_core_user(update: Update) -> bool:
    username = update.message.from_user.username

    #if not username in ACCOUNTS_CORE:
        #return False
    #return True
  
def obter_integrantes():
    """
    Obter o dicionário de integrantes e seus cargos.

    Returns:
        list[tuple[str, int, str, str]]: Lista de todos os integrantes do chat, no formato (nick, cargo_id, cargo_nome,
        telegram_username).
    """

    integrantes = [
        ("Esring", 1, "Membro", "@esring"),
        ("Bolus", 1, "Membro", "@bolus"),
        ("Bogrgoso", 7, "Presidência", "@bogrgoso"),
        ("Finwidir", 3, "Sub-Líder", "@finwidir"),
        ("Ledeon", 3, "Sub-Líder", "@ledeon"),
        ("Meinbao", 3, "Sub-Líder", "@meinbao"),
        ("Dyelo", 2, "Auxiliar", "@dyelo"),
        ("Uspok", 4, "Vice/Líder", "@uspo"),
        ("Rendîr", 4, "Vice/Líder", "@rendir"),
        ("Glanir", 1, "Membro", "@glanir"),
        ("Harro", 2, "Auxiliar", "@harro")
    ]
    integrantes.sort(key=lambda x: x[1])

    return integrantes


def obter_cargo_nome(cargo_id):
    """
    Obter o nome do cargo a partir do contador.

    Args:
        cargo_id (int): Id do cargo.

    Returns:
        str: Nome do cargo.
    """
    cargos_dicionario = {
        0: "Membro",
        1: "Auxiliar",
        2: "Sub-Líder",
        3: "Vice/Líder",
        4: "CORE",
        5: "Comando",
        6: "Presidência"
    }
    return cargos_dicionario[cargo_id]


def formatar_mensagem_integrantes(integrantes: list[tuple[str, int, str]]) -> str:
    """
    Formata a mensagem de integrantes para ser enviada.

    Args: integrantes (list[tuple[str, int, str]]): Lista de todos os integrantes do chat, no formato (nick,
    cargo_id, cargo_nome).

    Returns:
        str: Mensagem formatada com os integrantes e seus cargos.
    """
    mensagem = "Integrantes do chat:\n"

    #integrantes_agrupados = groupby(integrantes, key=lambda x: x[1])
    contador = 1

    while contador <= 7:
        cargo_nome = obter_cargo_nome(contador)
        vazio = True
        mensagem += f"<b>\n{cargo_nome}</b>:\n"
        for integrante in integrantes:
            if integrante[1] == contador:
                mensagem += f"    • {integrante[0]} - {integrante[3]}\n"
                vazio = False

        if vazio:
            mensagem += "-x-\n"

        contador += 1

    return mensagem

async def update_members_message(chat_id : int):
    bot = Bot("7843899651:AAGMnEzJ9cAhzzgizgMsiKdjMD8i8Ae6VF0")
    
    message = formatar_mensagem_integrantes(obter_integrantes())
    
    await bot.edit_message_text(message, chat_id, 635, parse_mode="HTML")
    
    