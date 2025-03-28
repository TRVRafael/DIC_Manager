from telegram import Update


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

def get_fancy_name(role_name : str) -> str:
    roles = {
        "membro": "Membro",
        "fiscal": "Fiscal",
        "auxiliar": "Auxiliar",
        "sublider": "Sub-Líder",
        "vicelider": "Vice-Líder",
        "lider": "Líder",
        "core": "CORE",
        "comando": "Comando",
        "comandogeral": "Comando-Geral",
        "presidencia": "Presidência"

    }
    return roles[role_name]

def obter_integrantes():
    """
    Obter o dicionário de integrantes e seus cargos.

    Returns:
        list[tuple[str, int, str]]: Lista de todos os integrantes do chat, no formato (nick, cargo_id, cargo_nome).
    """

    integrantes = [
        ("Esring", 1, "Membro"),
        ("Bolus", 1, "Membro"),
        ("Bogrgoso", 7, "Presidência"),
        ("Finwidir", 3, "Sub-Líder"),
        ("Ledeon", 3, "Sub-Líder"),
        ("Meinbao", 3, "Sub-Líder"),
        ("Dyelo", 2, "Auxiliar"),
        ("Uspok", 4, "Vice/Líder"),
        ("Rendîr", 4, "Vice/Líder"),
        ("Glanir", 1, "Membro"),
        ("Harro", 2, "Auxiliar"),
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
        1: "Membro",
        2: "Auxiliar",
        3: "Sub-Líder",
        4: "Vice/Líder",
        5: "CORE",
        6: "Comando",
        7: "Presidência"
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
                mensagem += f"    • {integrante[0]}\n"
                vazio = False

        if vazio:
            mensagem += "-x-\n"

        contador += 1

    return mensagem

