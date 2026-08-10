import logging
import time
from logging_config import configurar_logging
from extract import conexao_api_clientes
from load import importar_json_clientes, atualizar_processados
from transform import transformacao_clientes
from load_sql import insert_db
# from helpers import caminho_lista_processados

logger = logging.getLogger(__name__)

# testes = r"C:\Users\luiz_\OneDrive\Desktop\Engenharia_de_DadosV2\01-Projetos-2026\data-pipeline-usuarios\data\raw\2026-07-31T20-06-34-users.json"

def main():
    inicio = time.perf_counter()
    configurar_logging()

    try:
        logging.info("Pipeline iniciado")

        raw = conexao_api_clientes()

        if not raw or not raw.get("results"):
            raise RuntimeError("API não retornou dados válidos")

        #import_clientes = importar_json_clientes(testes)  

        import_clientes = importar_json_clientes(raw)

        insert = transformacao_clientes(import_clientes)

        insert_db(insert)

        atualizar_processados()

        logging.info("Status: Sucesso")

    except Exception:
        logging.exception("Status: Erro")
        raise

    finally:
        tempo_execucao = time.perf_counter() - inicio
        logging.info("Execução: %.2f segundos", tempo_execucao)
     
if __name__ == "__main__":
     main()













