import logging
from logging.handlers import RotatingFileHandler
from helpers import caminho_log, data_arquivo
import os

cm_log = caminho_log()
dt_arquivo = data_arquivo()

"""
logging.basicConfig( 
        level=logging.INFO, 
        format="", 
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=, 
        filemode="a", 
        encoding="utf-8")

logger = logging.getLogger(__name__)
logger.info( "Arquivo processado. arquivo = %s registros = %s", arquivo, total)

"""

def configurar_logging(): 

        log_file = f"{cm_log}/{dt_arquivo}-pipeline.log" 

        formatter = logging.Formatter( fmt=("%(asctime)s | %(levelname)s | %(funcName)s | %(message)s" ), datefmt="%Y-%m-%d %H:%M:%S")

        # Exibe logs no terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Salva logs em arquivo
        file_handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=5_000_000,
                backupCount=3,
                encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logging.basicConfig(
                level=logging.INFO,
                handlers=[
                console_handler,
                file_handler
                ],
                force=True )


