import json
import requests

def buscar_banco_de_cartas():

    lista_de_cartas = requests.get("https://api.scryfall.com/catalog/card-names")

    cartas = json.loads(lista_de_cartas.text)



    return cartas