import logging
from logging.handlers import RotatingFileHandler

from os import makedirs
from os.path import exists


class FilterHTTPLogs(logging.Filter):
    def filter(self, record):
        # Ignorar registros que contenham "HTTP Request" no nome do logger
        if "HTTP Request" in record.getMessage():
            return False
        return True


def setup_logging() -> None:
    """
    Configura o logging do bot para armazenar logs em um arquivo rotacionado.
    """
    
    # Cria o diretório de logs, caso não exista.
    if not exists('logs'):
        makedirs('logs')
    
    # Ajusta o logger do pacote 'telegram' para capturar apenas WARNINGS e erros mais graves
    logging.getLogger('telegram').setLevel(logging.WARNING)
    
    # Definição de um manipulador de arquivo rotacionado
    handler = RotatingFileHandler(
        'logs/bot.log', 
        maxBytes=5*1024*1024, 
        backupCount=5,
        encoding="utf-8"
    )
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)
    
    # Filtros
    handler.addFilter(FilterHTTPLogs())

    # Configuração do logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("Logging do bot iniciado.")