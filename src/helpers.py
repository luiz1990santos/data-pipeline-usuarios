import datetime 
from pathlib import Path

"""

    DRY -  DONT REPEAT YOURSELF.

    FUNÇÃO UTILITÁRIA DEVE SER CENTRALIZADA!

"""
BASE_DIR = Path(__file__).resolve().parent.parent


def caminho_raw_clientes():

    caminho = BASE_DIR / "data" / "raw"
    caminho.mkdir(parents=True, exist_ok=True)

    return caminho


def caminho_bronze_clientes():

    caminho = BASE_DIR / "data" / "bronze"
    caminho.mkdir(parents=True, exist_ok=True)

    return caminho


def caminho_silver_clientes():

    caminho = BASE_DIR / "data" / "silver"
    caminho.mkdir(parents=True, exist_ok=True)

    return caminho




def caminho_log():

    caminho = BASE_DIR / "log" 
    caminho.mkdir(parents=True, exist_ok=True)

    return caminho


def caminho_lista_processados():
    
    caminho = BASE_DIR / "data" / "pipeline_state"
    caminho.mkdir(parents=True, exist_ok=True)

    return caminho


def data_arquivo():
    # 1. Obtém o timestamp atual como inteiro
    timestamp_int = int(datetime.datetime.now().timestamp())

    # 2. Converte o inteiro para a data no formato solicitado
    data_formatada = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y-%m-%dT%H-%M-%S')

    return data_formatada 


def data_registro():
    # 1. Obtém o timestamp atual como inteiro
    timestamp_int = int(datetime.datetime.now().timestamp())

    # 1. Obtém o timestamp atual como inteiro
    data_atual = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y-%m-%d %H:%M:%S')

    return data_atual


