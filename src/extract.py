
import requests 
# import os
import logging
from uuid import uuid4
# from .logger import log

logger = logging.getLogger(__name__)


def conexao_api_clientes():

     try:
            url = 'https://randomuser.me/api'


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
           
            # REQUESICAO NA API POR GET
            response = requests.get(url, params=params, headers=headers, timeout=10)

            # Falha se HTTP for 4xx ou 5xx
            response.raise_for_status()     

            # Conversão a resposta para JSON
            data = response.json()
            #print(data)

            users = data.get("results", [])
            registros = len(users)


            if response.status_code == 200:
                # CONDICAO CASO A API NÃO ESTEJA RETORNANDO DADOS 
                if registros == 0:
                    logging.warning("API retornou lista vazia")
                    
                else:
                    logging.info('Recebidos API: %d', registros)
                    
            else:
                data = None 
                logging.error("API Sem retorno")   

            return data             

     except requests.JSONDecodeError as e:
          logging.error("Erro ao converter JSON: %s", e)
          raise

     except requests.ConnectTimeout:
          logging.error("Timeout na conexão")
          raise

     except requests.Timeout:
          logging.error("Tempo limite excedido da API")
          raise

     except requests.HTTPError:
          logging.error("HTTP Error")
          raise

     except requests.ConnectionError:
          logging.error("Erro na conexão")
          raise

     except requests.RequestException:
          logging.error("Erro durante a extração")
          raise

     except Exception as e:
          logging.error("Erro inesperado: %s, %s", type(e).__name__, e)
          raise
                




#Exibir o resultado (nome do usuário)
#teste = conexao_api_clientes()
#print(teste)


#import sys
#print(sys.version)