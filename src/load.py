
import json 
import logging
from helpers import data_arquivo, caminho_raw_clientes, caminho_lista_processados
import os

logger = logging.getLogger(__name__)

dt = data_arquivo()
cm_clientes = caminho_raw_clientes()



# print(cm)

def importar_json_clientes(dados):
    # print(data_formatada)
   try:
        # caminho = r"C:\Users\luiz_\OneDrive\Desktop\Engenharia_de_DadosV2\01-Projetos-2026\data-pipeline-usuarios\data\raw\2026-07-31T20-13-14-users.json"
        caminho = f'{cm_clientes}/{dt}-users.json'

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        logging.info("JSON criado com Sucesso")

   except NameError: 
        logging.error(f"Variável/nome inexistente")
        raise

   except FileNotFoundError:
        logging.exception("Caminho do arquivo não localizado")
        raise

   except Exception as e:
        logging.error(f"erro inesperado: {type(e).__name__}, {e}")
        raise

   return caminho

#print(registro_log)




def atualizar_processados():

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
