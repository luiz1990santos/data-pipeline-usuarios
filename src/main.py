from extract import conexao_api_clientes
from load import importar_json_clientes, atualizar_processados
from transform import transformacao_clientes
from load_sql import insert_db
# from helpers import caminho_lista_processados


raw = conexao_api_clientes()

import_clientes = importar_json_clientes(raw)


if raw and len(raw.get("results", [])) > 0:
     import_clientes 

# print(import_clientes)

insert = transformacao_clientes(import_clientes)


insert_db(insert)



arquivos_gerados = atualizar_processados()
















