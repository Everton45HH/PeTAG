import requests
import random
import time


if __name__ == '__main__':

    id = int(input("Digite o ID do usuario: "))
    id_coleira = int(input("Digite o ID da coleira: "))

    coleira = {
        "idColeira": id_coleira,
        "latitude": 0,
        "longitude": 0,
        "userID": id
    }

    url = f'http://192.168.18.10:5000/devices/{coleira["idColeira"]}/coords'

    while True:

        coleira["latitude"] += random.uniform(-0.0001, 0.0001)
        coleira["longitude"] += random.uniform(-0.00001, 0.0001)

        try:
            response = requests.put(url, json=coleira)
            print('Estou andando')
        
        except Exception as e:
            print("Erro")
            pass
        time.sleep(3)
    