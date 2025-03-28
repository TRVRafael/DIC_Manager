from telegram import Bot, Update
from telegram.ext import CallbackContext

from data import db_controller

def obter_integrantes():
    """
    Obter o dicionário de integrantes e seus cargos.

    Returns:
        list[tuple[str, int, str, str]]: Lista de todos os integrantes do chat, no formato (nick, cargo_id, cargo_nome,
        telegram_username).
    """

    # integrantes = [
    #     ("Esring", 0, "Membro", "@esring"),
    #     ("Bolus", 0, "Membro", "@bolus"),
    #     ("Bogrgoso", 6, "Presidência", "@bogrgoso"),
    #     ("Finwidir", 2, "Sub-Líder", "@finwidir"),
    #     ("Ledeon", 2, "Sub-Líder", "@ledeon"),
    #     ("Meinbao", 2, "Sub-Líder", "@meinbao"),
    #     ("Dyelo", 1, "Auxiliar", "@dyelo"),
    #     ("Uspok", 3, "Vice/Líder", "@uspo"),
    #     ("Rendîr", 4, "Vice/Líder", "@rendir"),
    #     ("Glanir", 0, "Membro", "@glanir"),
    #     ("Harro", 1, "Auxiliar", "@harro")
    # ]
    # integrantes.sort(key=lambda x: x[1])
    integrantes = db_controller.get_members_list()
    print(integrantes)

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
        3: "Vice",
        4: "Líder",
        5: "CORE",
        6: "Comando",
        7: "Comando-Geral",
        8: "Presidência",
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
    contador = 0

    while contador <= 8:
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
    bot = Bot("7827037297:AAGgeHSy3tZI_tCPpH3ujB4jdgV_L37yvvE")
    
    message = formatar_mensagem_integrantes(obter_integrantes())
    try:
        await bot.edit_message_text(message, chat_id, 10, parse_mode="HTML")
    except Exception:
        pass
    
async def force_members_message_update(update: Update, context = CallbackContext):
    await update_members_message(update.effective_chat.id)