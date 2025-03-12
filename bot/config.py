from os import getenv
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

ACCOUNTS_CORE = ["torvi_hb", "kprand", "ysetheus", "helpier011", "golerobom196", "valenteb1", "gbgmss", "Tarkeru", "crucisx", "slcaiodev"]
BOT_TOKEN = getenv("BOT_TOKEN")
PERMISSIONED_GROUP_ID = getenv("PERMISSIONED_GROUP_ID")