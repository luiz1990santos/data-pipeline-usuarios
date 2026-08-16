#import time
#from helpers import run_id
#from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import pyodbc
import os

"""
    run = run_id()
    inicio = time.perf_counter()
    inicio_hora = datetime.now()
    inicio_hora2 = inicio_hora.strftime('%Y-%m-%d %H:%M:%S')
    fim_hora = datetime.now()
    fim_hora2 = fim_hora.strftime('%Y-%m-%d %H:%M:%S')
    status = "Sucesso"
    tempo_execucao = time.perf_counter() - inicio
    erro = "NULL"
"""

def runs_pipeline(run_id,inicio_hora2,fim_hora2,status,tempo_execucao,erro):

    lista_runs = {"run_id":run_id,"inicio_hora":inicio_hora2,"fim_hora":fim_hora2,"status":status,"tempo_execucao":tempo_execucao, "erro":erro}


    return([lista_runs]) 


def insert_pipeline_runs(lista_runs):
    conexao = None
    df = pd.DataFrame(lista_runs)

    print(df)

    load_dotenv()

    conexao = pyodbc.connect(
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED')};"
    )


    cursor = conexao.cursor()

    data = [
                tuple(None if pd.isna(valor) else valor for valor in linha)
                for linha in df.itertuples(index=False, name=None)
        ]

    cursor.executemany( """
                
                INSERT INTO PIPELINE_RUNS ( run_id,
                                            started_at,
                                            finished_at,
                                            status,
                                            duration_seconds,
                                            error_message)
                            
                VALUES (?, ?, ?, ?, ?, ?)
                            
        """, data)

    conexao.commit()



def update_pipeline_runs(lista_runs):
    conexao = None
    df = pd.DataFrame(lista_runs)

    print(df)

    # RECOLOCAR O """ NO CURSOR!!!!!!

    load_dotenv()

    conexao = pyodbc.connect(
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED')};"
    )


    cursor = conexao.cursor()

    update = """
                
                UPDATE PIPELINE_RUNS 
                SET  
                    finished_at = ?,
                    status = ?,
                    duration_seconds = ?,
                    error_message = ?

                WHERE run_id = ?
                            
        """

    cursor.execute(
        update,
        df['fim_hora'].iloc[0],
        df['status'].iloc[0],
        df['tempo_execucao'].iloc[0],
        df['erro'].iloc[0],
        df['run_id'].iloc[0]
    )

    conexao.commit()


#pp = runs_pipeline(run,inicio_hora2,fim_hora2,status,tempo_execucao,erro)
#print(pp)

#insert_pipeline_runs(pp) 