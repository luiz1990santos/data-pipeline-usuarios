from extract import conexao_api_clientes
from load import importar_json_clientes, atualizar_processados
from transform import transformacao_clientes
# from helpers import caminho_lista_processados


raw = conexao_api_clientes()

import_clientes = None

if raw and len(raw.get("results", [])) > 0:
     import_clientes = importar_json_clientes(raw)

# print(import_clientes)

transformacao_clientes(import_clientes)




arquivos_gerados = atualizar_processados()
















