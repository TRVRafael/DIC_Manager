import logging
from logging.handlers import RotatingFileHandler

import os


class FilterHTTPLogs(logging.Filter):
    def filter(self, record):
        if "HTTP Request" in record.getMessage():
            return False
        return True
    
    
def setup_logging(name: str, log_file: str) -> logging.Logger:
    """
    Configura o logging do bot para armazenar logs em um arquivo rotacionado.
    """
    
    # Make sure dir exists
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    # Definição de um manipulador de arquivo rotacionado
    handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024, 
        backupCount=5,
        encoding="utf-8"
    )
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)
    
    # Filtros
    handler.addFilter(FilterHTTPLogs())

    # Configuração do logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.hasHandlers():
        logger.addHandler(handler)

    logger.info(f"Logger '{name}' started.")
    return logger

bot_logger = setup_logging("bot", "logs/bot.log")