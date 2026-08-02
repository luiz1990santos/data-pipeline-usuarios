import pandas as pd
import re
import json
from helpers import caminho_bronze_clientes, data_arquivo, data_registro, run_id
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

data_arquivo = data_arquivo()

data_registro = data_registro()

caminho_bronze = caminho_bronze_clientes()

run_id = run_id()

PADRAO_EMAIL = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def transformacao_clientes(arquivo):
    # volume_csv = 0
    logging.info('Execução: %s', run_id)
    logging.info('Iniciando criação do CSV')

    try:
        caminho = str(caminho_bronze)

        nome_arquivo = str(data_arquivo)

        # print(data_arquivo)

        with open(arquivo, "r", encoding="utf-8") as a:
            dados = json.load(a)

        usuarios = dados.get("results", [])

        usuarios_csv = list()
        
        for usuario in usuarios:

            data_nascimento = usuario.get("dob", {}).get("date")
            id = usuario.get("login", {}).get("uuid")
            email = usuario.get("email")

            if (id and re.fullmatch(PADRAO_EMAIL, email) is not None and datetime.fromisoformat(data_nascimento.replace("Z", "+00:00")).date() <= date.today()):
                usuario_valido = {
                    "run_id": run_id,
                    "id": usuario.get("login", {}).get("uuid"),
                    "first_name": usuario.get("name", {}).get("first"),
                    "last_name": usuario.get("name", {}).get("last"),
                    "gender": usuario.get("gender"),
                    "email": usuario.get("email"),
                    "cpf": usuario.get("id",{}).get("value"),
                    "street": usuario.get("location", {}).get("street", {}).get("name"),
                    "number": usuario.get("location", {}).get("street", {}).get("number"),
                    "city": usuario.get("location", {}).get("city"),
                    "state": usuario.get("location", {}).get("state"),
                    "country": usuario.get("location", {}).get("country"),
                    "latitude": usuario.get("location", {}).get("coordinates", {}).get("latitude"),
                    "longitude": usuario.get("location", {}).get("coordinates", {}).get("longitude"),
                    "date_of_birth": usuario.get("dob", {}).get("date"),
                    "age": usuario.get("dob", {}).get("age"),
                    "registration_date": usuario.get("registered", {}).get("date"),
                    "regist_age": usuario.get("registered", {}).get("age"),
                    "created_at": data_registro,
                    "validacao": "OK"
                }

                usuarios_csv.append(usuario_valido)                
                 
            else:
                usuario_invalido = {
                    "run_id": run_id,
                    "id": usuario.get("login", {}).get("uuid"),
                    "first_name": usuario.get("name", {}).get("first"),
                    "last_name": usuario.get("name", {}).get("last"),
                    "gender": usuario.get("gender"),
                    "email": usuario.get("email"),
                    "cpf": usuario.get("id",{}).get("value"),
                    "street": usuario.get("location", {}).get("street", {}).get("name"),
                    "number": usuario.get("location", {}).get("street", {}).get("number"),
                    "city": usuario.get("location", {}).get("city"),
                    "state": usuario.get("location", {}).get("state"),
                    "country": usuario.get("location", {}).get("country"),
                    "latitude": usuario.get("location", {}).get("coordinates", {}).get("latitude"),
                    "longitude": usuario.get("location", {}).get("coordinates", {}).get("longitude"),
                    "date_of_birth": usuario.get("dob", {}).get("date"),
                    "age": usuario.get("dob", {}).get("age"),
                    "registration_date": usuario.get("registered", {}).get("date"),
                    "regist_age": usuario.get("registered", {}).get("age"),
                    "created_at": data_registro,
                    "validacao": "NOK"
                }                
                usuarios_csv.append(usuario_invalido)

        json_normalizado = pd.json_normalize(usuarios_csv)

        arquivo_saida = f"{caminho}/{nome_arquivo}-users.csv"

        csv = f"{nome_arquivo}-users.csv"

        json_normalizado.to_csv(arquivo_saida, index = False)

        registro_validos = len(json_normalizado[json_normalizado["validacao"] == "OK"])
        registro_invalidos = len(json_normalizado[json_normalizado["validacao"] == "NOK"])
        qtd_distinta = json_normalizado.loc[json_normalizado["id"] != "","id"].nunique()

        if not registro_validos or registro_validos <= 0:
            logging.error('Arquivo criado vazio')
        else:
            logging.info('CSV criado com sucesso - "%s"', csv) 
            logging.info('Validos: %d', registro_validos)
            logging.warning('Invalidos: %d', registro_invalidos) 
            logging.info('IDs distintos: %d', qtd_distinta)

            

    except UnboundLocalError:
        logging.error(f"Não foi possivel acessar a variável local")

    except Exception as e:
        logging.error(f"erro inesperado: {type(e).__name__}")  

    return arquivo_saida



#teste = transformacao_clientes()

#print(teste)

# dataset = pd.json_normalize(teste)


# print(dataset.dtypes)



# print(dataset.describe())


# csv = dataset.to_csv