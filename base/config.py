from os import getenv
from dotenv import load_dotenv
import json

# Carregar variáveis do .env
load_dotenv()

def load_bot_tokens():
    """Carrega e parseia os tokens do .env"""
    tokens_json = getenv("BOT_TOKENS", "{}")
    try:
        return json.loads(tokens_json)
    except json.JSONDecodeError:
        raise ValueError("Formato inválido para BOT_TOKENS no .env")

BOT_TOKENS = load_bot_tokens()

ACCOUNTS_CORE = ["torvi_hb", "kprand", "ysetheus", "helpier011", "golerobom196", "valenteb1", "gbgmss", "Tarkeru", "crucisx", "slcaiodev"]
PERMISSIONED_GROUP_ID = getenv("PERMISSIONED_GROUP_ID")

MEMBERS_CONTROL_MESSAGES = {
    "em": {"chat_id":"-1002695748985", "message_id": "11032"},
    "sp": {"chat_id":"-1002557197490", "message_id": "22"},
}