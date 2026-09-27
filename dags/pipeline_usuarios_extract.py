from airflow.sdk import dag, task, TriggerRule
import pendulum
from datetime import datetime
from run_control import runs_pipeline, insert_pipeline_runs, update_pipeline_runs
from extract import conexao_api_clientes
from load import importar_json_clientes
from transform import transformacao_clientes
from load_sql import insert_db
from helpers import run_id


@dag(

        dag_id="pipeline_usuarios_extract",
        schedule=None,
        start_date=pendulum.datetime(2026, 8, 30, tz="America/Sao_Paulo"),
        catchup=False,
    )


def pipeline_usuarios_extract():
    @task
    def start_run():
        novo_run_id = run_id()

        inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        registro = runs_pipeline(novo_run_id,inicio,None,"RUNNING",None,None)

        insert_pipeline_runs(registro)

        print(f"Run ID: {novo_run_id}")

        return {
            "run_id": novo_run_id,
            "started_at": inicio
        }


    @task
    def extract_raw(metadata_start):
        run_id_execucao = metadata_start["run_id"]

        dados = conexao_api_clientes()
        qtd_registro = dados.get("results", [])

        caminho_raw = importar_json_clientes(dados)

        print(f"Extração concluída: {len(qtd_registro)}")
        print(f"Arquivo Raw: {caminho_raw}")
        print(f"Run ID: {run_id_execucao}")

        return {
            "caminho_raw": str(caminho_raw),
            "run_id": run_id_execucao
        }

    @task
    def transform_bronze(metadata):

       caminho_raw = metadata["caminho_raw"]
       run_id_execucao = metadata["run_id"]

       # raise RuntimeError("Falha controlada Airflow 11")

       caminho_bronze = transformacao_clientes(caminho_raw,run_id_execucao)

       print(f"Arquivo Bronze: {caminho_bronze}")
       print(f"Run ID: {run_id_execucao}")

       return {
            "caminho_bronze": str(caminho_bronze),
            "run_id": run_id_execucao
        }


    @task
    def load_sql(metadata):
        caminho_bronze = metadata["caminho_bronze"]
        run_id_execucao = metadata["run_id"]

        insert_db(caminho_bronze, run_id_execucao)       


    @task
    def finalize_success(metadata_start, resultado_carga):
        run_id_execucao = metadata_start["run_id"]
        inicio = metadata_start["started_at"]

        fim_dt = datetime.now()
        fim = fim_dt.strftime("%Y-%m-%d %H:%M:%S")

        inicio_dt = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
        duracao = (fim_dt - inicio_dt).total_seconds()

        registro = runs_pipeline(run_id_execucao,inicio,fim,"SUCCESS",duracao,None)

        update_pipeline_runs(registro)


    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def finalize_error(metadata_start):
        run_id_execucao = metadata_start["run_id"]
        inicio = metadata_start["started_at"]

        fim_dt = datetime.now()
        fim = fim_dt.strftime("%Y-%m-%d %H:%M:%S")

        inicio_dt = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
        duracao = (fim_dt - inicio_dt).total_seconds()

        mensagem_erro = "Falha em uma etapa do pipeline Airflow"

        registro = runs_pipeline(
            run_id_execucao,
            inicio,
            fim,
            "ERROR",
            duracao,
            mensagem_erro
        )

        update_pipeline_runs(registro)

        raise RuntimeError(mensagem_erro) 


    metadata_start = start_run()

    metadata_raw = extract_raw(metadata_start)

    metadata_bronze = transform_bronze(metadata_raw)

    resultado_carga = load_sql(metadata_bronze)

    finalize_success(metadata_start, resultado_carga)

    erro = finalize_error(metadata_start)

    metadata_raw >> erro
    metadata_bronze >> erro
    resultado_carga >> erro
    

pipeline_usuarios_extract()






