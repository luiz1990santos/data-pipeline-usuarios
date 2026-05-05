from extract import conexao_api_clientes
from load import importar_json_clientes, lista_arquivos
#from transform import import_json_normalizado
from helpers import caminho_lista_processados


clientes= conexao_api_clientes()


#print(api['results'])

if clientes is not None or len(clientes['results']) > 0:
     import_clientes = importar_json_clientes(clientes)

# normalizado = import_json_normalizado()


arquivos_gerados = lista_arquivos()















