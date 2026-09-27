from airflow.sdk import dag, task
import pendulum
from extract import conexao_api_clientes
from load import importar_json_clientes
from transform import transformacao_clientes
from helpers import run_id


@dag(

        dag_id="pipeline_usuarios_extract",
        schedule=None,
        start_date=pendulum.datetime(2026, 8, 30, tz="America/Sao_Paulo"),
        catchup=False,
    )


def pipeline_usuarios_extract():

    @task
    def extract_raw():
        dados = conexao_api_clientes() 
        qtd_registro = dados.get("results", [])

        caminho_raw = importar_json_clientes(dados)

        novo_run_id = run_id()

        print(f'Extração concluída: {len(qtd_registro)}')
        print(f"Arquivo Raw: {caminho_raw}")
        print(f"Run ID: {novo_run_id}")

        return {
            "caminho_raw": caminho_raw,
            "run_id": novo_run_id
        }
       

    @task
    def transform_bronze(metadata):

       caminho_raw = metadata["caminho_raw"]
       run_id_execucao = metadata["run_id"]

       caminho_bronze = transformacao_clientes(caminho_raw,run_id_execucao)

       print(f"Arquivo Bronze: {caminho_bronze}")
       print(f"Run ID: {run_id_execucao}")


    metadata = extract_raw()

    transform_bronze(metadata)
    

pipeline_usuarios_extract()






