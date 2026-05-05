
import requests 
import os
from logger import log
# from .logger import log

api_key = os.getenv("API_KEY")

# api_key = os.environ

#print(api_key)

def conexao_api_clientes():

        try:
            # Chave de acesso e a URL
            api_key = os.getenv("API_KEY")

            if not api_key:
                 raise ValueError("API_KEY não definida!")

            url = 'https://randomuser.me/api/'


            # Conf os parâmetros da requisição (opcional)
            params = {
                'results': 20,  # Quantidade de usuários
                'nat': 'br'    # Nacionalidade
            }

            # Config cabeçalho com a chave de API
            headers = {
                'Authorization': f'Bearer {api_key}',
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
                    data = response.json()
            else:
                data is None 
                log("ERROR", "API Sem retorno", "extract")            
        except Exception as e:
            data
            f"erro inesperado: {type(e).__name__}, {e}", "extract"

           

        return data




#Exibir o resultado (nome do usuário)
#teste = conexao_api_clientes()
#print(teste)



"""    # 6. Verifique se a requisição foi bem-sucedida (status 200)
            if response.status_code == 200:
                # CONDICAO CASO A API NÃO ESTEJA RETORNANDO DADOS 
                if len(user) == 0:
                    log("WARNING", "API retornou lista vazia", "extract")
                    
                else:
                    log("INFO", "Iniciando extração", "extract")
                    data = response.json()
            else:
                data is None 
                log("ERROR", "API Sem retorno", "extract")

            
"""


#import sys
#print(sys.version)