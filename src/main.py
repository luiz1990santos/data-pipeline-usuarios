import logging
from logging_config import configurar_logging
from extract import conexao_api_clientes
from load import importar_json_clientes, atualizar_processados
from transform import transformacao_clientes
from load_sql import insert_db
# from helpers import caminho_lista_processados

logger = logging.getLogger(__name__)

def main():
     configurar_logging()

     logging.info('Pipeline iniciado')


     raw = conexao_api_clientes()

     import_clientes = importar_json_clientes(raw)


     if raw and len(raw.get("results", [])) > 0:
          import_clientes 

     # print(import_clientes)

     insert = transformacao_clientes(import_clientes)


     insert_db(insert)


     # TESTE DE REPROCESSAMENTO
     #insert_db(r"C:\Users\luiz_\OneDrive\Desktop\Engenharia_de_DadosV2\01-Projetos-2026\data-pipeline-usuarios\data\bronze\2026-07-27T20-53-22-users.csv")


     arquivos_gerados = atualizar_processados()

     logging.info('Status: Sucesso')

if __name__ == "__main__":
     main()













