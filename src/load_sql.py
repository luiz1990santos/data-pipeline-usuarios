import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv


def insert_db(csv): 
    df = pd.read_csv(fr'{csv}')
    # print(df)

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
        INSERT INTO STAGING_USERS ( ID, 
                                    first_name,	
                                    last_name, 
                                    gender,	
                                    email, 
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
                       
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       
    """, data)

    # cursor.commit()

    sql_merge = """
                        
            WITH ORIGEM_FILTRADA AS (
                SELECT *,
                    -- Cria um ranking para cada ID. O número 1 será o registro mais recente (ou o primeiro encontrado)
                    ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at DESC) as RN
                FROM STAGING_USERS
            )
            MERGE SILVER_USERS AS DESTINO 
            -- CTE filtrada como origem, pegando apenas o registro único (RN = 1)
            USING (SELECT * FROM ORIGEM_FILTRADA WHERE RN = 1) AS ORIGEM
            ON (DESTINO.ID = ORIGEM.ID)

            WHEN NOT MATCHED THEN 
                INSERT( id, 	
                        first_name,	
                        last_name,	
                        gender,	
                        email,	
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
                
                VALUES( ORIGEM.id, 	
                        ORIGEM.first_name,	
                        ORIGEM.last_name,	
                        ORIGEM.gender,	
                        ORIGEM.email,	
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
                        ORIGEM.created_at);



        """

    try:
        cursor.execute(sql_merge)
        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        raise erro