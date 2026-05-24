
import requests 
import os
from logger import log
# from .logger import log



def conexao_api_clientes():

        try:

            url = 'https://randomuser.me/api/'


            # Conf os parâmetros da requisição (opcional)
            params = {
                'results': 20,  # Quantidade de usuários
                'nat': 'br'    # Nacionalidade
            }

            # Config cabeçalho com a chave de API
            headers = {
                #'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }


            data = str()
            
            # REQUESICAO NA API POR GET
            response = requests.get(url, params=params, headers=headers)
            
            # Conversão a resposta para JSON
            data = response.json()

            user = data.get("results", [])

            if response.status_code == 200:
                # CONDICAO CASO A API NÃO ESTEJA RETORNANDO DADOS 
                if len(user) == 0:
                    log("WARNING", "API retornou lista vazia", "extract")
                    
                else:
                    log("INFO", "Iniciando extração", "extract")
                    
            else:
                data = None 
                log("ERROR", "API Sem retorno", "extract")            
        except Exception as e:
            log("ERROR", f"Erro inesperado: {type(e).__name__}, {e}", "extract")
            return None

           

        return data




#Exibir o resultado (nome do usuário)
#teste = conexao_api_clientes()
#print(teste)


#import sys
#print(sys.version)