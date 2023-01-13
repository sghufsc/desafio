""" 
Configuração básica do client do MondoDB
"""

from pymongo import MongoClient, errors as pymongo_errors
from server.settings import MONGO_USER, MONGO_PASSWORD, MONGO_URL

def db():
    """ 
    Instância do banco MongoDB 
    Returns:
        client: Instância de client do MongoDB
    """

    client = MongoClient(MONGO_URL)

    try:
        # Verificando conexão do MongoDB
        client.server_info()

    except pymongo_errors.ServerSelectionTimeoutError as error:
        print(error)

    except Exception as error:
        print(error)

    return client['desafio']