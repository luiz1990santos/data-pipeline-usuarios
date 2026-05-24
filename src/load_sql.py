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
        INSERT INTO STAGING_USERS ( ID, first_name,	last_name, gender,	email, street, number, city, state, country, latitude, longitude, date_of_birth, age, registration_date, regist_age, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    cursor.commit()