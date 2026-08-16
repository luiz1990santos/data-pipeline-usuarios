import logging
import time
from datetime import datetime
from logging_config import configurar_logging
from extract import conexao_api_clientes
from load import importar_json_clientes, atualizar_processados
from transform import transformacao_clientes
from load_sql import insert_db
from helpers import run_id
from run_control import runs_pipeline, insert_pipeline_runs, update_pipeline_runs

logger = logging.getLogger(__name__)


# testes = r"C:\Users\luiz_\OneDrive\Desktop\Engenharia_de_DadosV2\01-Projetos-2026\data-pipeline-usuarios\data\raw\2026-07-31T20-06-34-users.json"

def main():
    inicio = time.perf_counter()
    inicio_hora = datetime.now()
    inicio_hora2 = inicio_hora.strftime('%Y-%m-%d %H:%M:%S')
    status = 'RUNNING'
    novo_run_id = run_id()
    erro = None
    houve_erro_pipeline = False


    configurar_logging()

    rp = runs_pipeline(novo_run_id, inicio_hora2, None, status, None, None)

    insert_pipeline_runs(rp)    

    try:
        logging.info("Pipeline iniciado")
        logging.info('Execução: %s', novo_run_id)

        raw = conexao_api_clientes()

        if not raw or not raw.get("results"):
            raise RuntimeError("API não retornou dados válidos")

        #import_clientes = importar_json_clientes(testes)  

        import_clientes = importar_json_clientes(raw)

        insert = transformacao_clientes(import_clientes, novo_run_id)

        insert_db(insert, novo_run_id)

        atualizar_processados()

        logging.info("Status: Sucesso")
        status = "SUCCESS"
        erro = None


    except Exception as e:
        houve_erro_pipeline = True
        status = "ERROR"
        erro = str(e)
        logging.exception("Status: Erro")
        raise

    finally:
        tempo_execucao = time.perf_counter() - inicio
        fim_hora = datetime.now()
        fim_hora2 = fim_hora.strftime('%Y-%m-%d %H:%M:%S')

        logging.info("Execução: %.2f segundos", tempo_execucao)

        rp = runs_pipeline(novo_run_id, inicio_hora2, fim_hora2, status, tempo_execucao, erro)
        try: 
            update_pipeline_runs(rp)          
        except Exception:
            logging.exception("Falha ao atualizar PIPELINE_RUNS")

            if not houve_erro_pipeline:
                raise    

        #print(f"inicio {inicio_hora.strftime('%Y-%m-%d %H:%M:%S')}")
        #print(f"fim {fim_hora.strftime('%Y-%m-%d %H:%M:%S')}")


        #print(rp)

if __name__ == "__main__":
     main()

