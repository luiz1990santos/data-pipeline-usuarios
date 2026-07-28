import pandas as pd
import json
from helpers import caminho_bronze_clientes, data_arquivo, data_registro, run_id
from logger import log


data_arquivo = data_arquivo()

data_registro = data_registro()

caminho_bronze = caminho_bronze_clientes()

run_id = run_id()

def transformacao_clientes(arquivo):
    try:
        caminho = str(caminho_bronze)

        nome_arquivo = str(data_arquivo)

        # print(data_arquivo)

        with open(arquivo, "r", encoding="utf-8") as a:
            dados = json.load(a)

        usuarios = dados.get("results", [])

        usuarios_transformados = []

        for usuario in usuarios:
            usuario_transformado = {
                "run_id": run_id,
                "id": usuario.get("login", {}).get("uuid"),
                "first_name": usuario.get("name", {}).get("first"),
                "last_name": usuario.get("name", {}).get("last"),
                "gender": usuario.get("gender"),
                "email": usuario.get("email"),
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
                "created_at": data_registro
            }

            usuarios_transformados.append(usuario_transformado)

        json_normalizado = pd.json_normalize(usuarios_transformados)

        arquivo_saida = f"{caminho}/{nome_arquivo}-users.csv"

        json_normalizado.to_csv(arquivo_saida, index = False)
        log("INFO", f"Arquivo {data_arquivo}-users.csv criado com Sucesso", "transform")
    except Exception as e:
        log("ERROR", f"erro inesperado: {type(e).__name__}, {e}", "transform")       

    return arquivo_saida



#teste = transformacao_clientes()

#print(teste)

# dataset = pd.json_normalize(teste)


# print(dataset.dtypes)



# print(dataset.describe())


# csv = dataset.to_csv