
import requests 
import os
import logging
from uuid import uuid4
# from .logger import log

logger = logging.getLogger(__name__)

def conexao_api_clientes():

        try:
            url = 'https://randomuser.me/api/'


            # Conf os parâmetros da requisição (opcional)
            params = { 
                       'results': 100,  # Quantidade de usuários
                       'nat': 'br'    # Nacionalidade 
                     }

            # Config cabeçalho com a chave de API
            headers = { #'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json' 
                      }

            logging.info('Iniciado a extração')
            #logging.debug("URL da chamada: ", url)
            #logging.debug('Parametros: ', params)

            data = str()
           
            # REQUESICAO NA API POR GET
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            # Conversão a resposta para JSON
            data = response.json()

            users = data.get("results", [])

            registros = len(users)

            if response.status_code == 200:
                # CONDICAO CASO A API NÃO ESTEJA RETORNANDO DADOS 
                if registros == 0:
                    logging.warning("API retornou lista vazia")
                    
                else:
                    logging.info('Extração Concluída - Registros: %d', registros)
                    
            else:
                data = None 
                logging.error("API Sem retorno")            

        except Exception as e:
            logging.error(f"Erro inesperado: {type(e).__name__}, {e}")
            return None

        except requests.Timeout:
             logging.error('Tempo limite excedido da API')

        except requests.RequestException:
             logging.exception('Erro durante a extração')
             raise            

        return data




#Exibir o resultado (nome do usuário)
#teste = conexao_api_clientes()
#print(teste)


#import sys
#print(sys.version)