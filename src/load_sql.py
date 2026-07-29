import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def insert_db(csv): 
    logging.info('Acesso ao DB')
    df = pd.read_csv(fr'{csv}')
    # print(df)

    run_id = df['run_id'].drop_duplicates()[0]

    # print(run_id)

    load_dotenv()

    conexao = pyodbc.connect(
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED')};"
    )


    cursor = conexao.cursor()

    # cursor.execute("SELECT * from STAGING_USERS")

    # for row in cursor:
        # print(row)

    data = list(df.itertuples(index=False, name=None))

    cursor.executemany("""
        INSERT INTO STAGING_USERS ( run_id,
                                    id, 
                                    first_name,	
                                    last_name, 
                                    gender,	
                                    email, 
                                    cpf,
                                    street, 
                                    number, 
                                    city, 
                                    state, 
                                    country, 
                                    latitude, 
                                    longitude, 
                                    date_of_birth, 
                                    age, 
                                    registration_date, 
                                    regist_age, 
                                    created_at)
                       
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       
    """, data)

    sql_merge =  f"""
                       WITH ORIGEM_FILTRADA AS (
                            SELECT *,
                                -- Cria um ranking para cada ID. O número 1 será o registro mais recente (ou o primeiro encontrado)
                                ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at DESC) as RN
                            FROM STAGING_USERS
                            WHERE RUN_ID = ?
                        ) 
                        MERGE SILVER_USERS AS DESTINO 
                        -- Agora usamos a CTE filtrada como origem, pegando apenas o registro único (RN = 1)
                        USING ( SELECT * FROM ORIGEM_FILTRADA
                                WHERE RN = 1) AS ORIGEM
                        ON (DESTINO.ID = ORIGEM.ID)

                        WHEN NOT MATCHED THEN 
                            INSERT( run_id,
                                    id, 	
                                    first_name,	
                                    last_name,	
                                    gender,	
                                    email,
                                    cpf,	
                                    street,	
                                    number,	
                                    city,	
                                    state,	
                                    country,	
                                    latitude,	
                                    longitude,	
                                    date_of_birth,	
                                    age,	
                                    registration_date,	
                                    regist_age,
                                    created_at  )
                            
                            VALUES( ORIGEM.run_id,
                                    ORIGEM.id, 	
                                    ORIGEM.first_name,	
                                    ORIGEM.last_name,	
                                    ORIGEM.gender,	
                                    ORIGEM.email,
                                    ORIGEM.cpf,	
                                    ORIGEM.street,	
                                    ORIGEM.number,	
                                    ORIGEM.city,	
                                    ORIGEM.state,	
                                    ORIGEM.country,	
                                    ORIGEM.latitude,	
                                    ORIGEM.longitude,	
                                    ORIGEM.date_of_birth,	
                                    ORIGEM.age,	
                                    ORIGEM.registration_date,	
                                    ORIGEM.regist_age,
                                    TRY_CONVERT(DATETIME2(0), ORIGEM.created_at, 120)   )
                                    
                        ;

    """

    try:

        cursor.execute(sql_merge, run_id)
        conexao.commit()

        qry_staging = f'SELECT COUNT(*) FROM STAGING_USERS WHERE RUN_ID = ?;'

        cursor.execute(qry_staging, run_id)
        registros_staging = cursor.fetchall()[0][0]


        qry_silver = f'SELECT COUNT(*) FROM SILVER_USERS WHERE RUN_ID = ?;'

        cursor.execute(qry_silver, run_id)
        registros_silver = cursor.fetchall()[0][0]

        logging.info('Insert STAGING_USERS - Registros: %d', registros_staging)
        logging.info('Insert SILVER_USERS - Registros: %d', registros_silver)


    except Exception as erro:
        logging.error(f"erro inesperado: {type(erro).__name__}") 
        conexao.rollback()
        raise erro







