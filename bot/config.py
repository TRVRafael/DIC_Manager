from os import getenv
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")