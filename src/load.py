
import json 
from logger import log
from helpers import data_arquivo, caminho_raw_clientes, caminho_lista_processados
import os


dt = data_arquivo()
cm_clientes = caminho_raw_clientes()

# print(cm)

def importar_json_clientes(dados):


    # print(data_formatada)
    try:
        caminho = f'{cm_clientes}/{dt}-clientes.json'

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        log("INFO", f"Arquivo {dt}_clientes.json criado com Sucesso", "load")
    except Exception as e:
        log("ERROR", f"erro inesperado: {type(e).__name__}, {e}", "load")

    return caminho

#print(registro_log)




def lista_arquivos():

    arquivos = os.listdir(cm_clientes)

    arquivo_apend = caminho_lista_processados()

    caminho_completo = os.path.join(arquivo_apend, "processed_files.txt")

    processados_antes = set()

    # print(caminho_completo)

    # 1. Ler os arquivos que JÁ FORAM processados (se o arquivo existir)
    if os.path.exists(caminho_completo):    
        with open(caminho_completo, "r", encoding="utf-8") as r:
            # .strip() remove o \n para a comparação ficar limpa
            processados_antes = {linha.strip() for linha in r}

    # 2. Abrir para adicionar (append) apenas os novos
    with open(caminho_completo, "a", encoding="utf-8") as t:
        for arquivo in arquivos:
            if arquivo not in processados_antes:
                t.write(f"{arquivo}\n")
            else: 
                pass


    return processados_antes


# print(lista_arquivos())



"""
def transformacao_clientes(cm_clientes):

    with open(cm_clientes, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    usuarios = dados.get("results", [])

    usuarios_transformados = []

    for usuario in usuarios:
        usuario_transformado = {
            "id": usuario.get("login", {}).get("uuid"),
            "first_name": usuario.get("name", {}).get("first"),
            "last_name": usuario.get("name", {}).get("last"),
            "gender": usuario.get("gender"),
            "email": usuario.get("email"),
            "street": usuario.get("street", {}).get("name"),
            "number": usuario.get("street", {}).get("number"),
            "city": usuario.get("location", {}).get("city"),
            "state": usuario.get("location", {}).get("state"),
            "country": usuario.get("location", {}).get("country"),
            "latitude": usuario.get("coordinates", {}).get("latitude"),
            "longitude": usuario.get("coordinates", {}).get("longitude"),
            "date_of_birth": usuario.get("dob", {}).get("date"),
            "age": usuario.get("dob", {}).get("age"),
            "registration_date": usuario.get("registered", {}).get("date"),
            "regist_age": usuario.get("registered", {}).get("age")
        }

        usuarios_transformados.append(usuario_transformado)

    return usuarios_transformados
"""