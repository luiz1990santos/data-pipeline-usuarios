from airflow.sdk import dag, task
import pendulum
from extract import conexao_api_clientes


@dag(

        dag_id="pipeline_usuarios_extract",
        schedule=None,
        start_date=pendulum.datetime(2026, 8, 30, tz="America/Sao_Paulo"),
        catchup=False,
    )


def pipeline_usuarios_extract():

    @task
    def extract():
        conexao = conexao_api_clientes() 
        qtd_registro = conexao.get("results", [])
        print(f'Extração concluída: {len(qtd_registro)}')
        


    dados_extraidos = extract()

    

pipeline_usuarios_extract()






