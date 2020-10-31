# coding=utf8

import json
import requests


class ListaCartasService:

    def __init__(self):
        self.cartas = None

    def buscar_cartas_scryfall(self):
        lista_de_cartas = requests.get("https://api.scryfall.com/catalog/card-names")
        self.cartas = json.loads(lista_de_cartas.text)['data']
        return self.cartas
