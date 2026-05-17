import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

conexao = pyodbc.connect(
    f"DRIVER={os.getenv('DB_DRIVER')};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"Trusted_Connection={os.getenv('DB_TRUSTED')};"
)


cursor = conexao.cursor()

cursor.execute("SELECT TOP 10 * from BO_2016")

select = cursor.fetchone()


print(select)