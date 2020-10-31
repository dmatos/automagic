# coding=utf8

import time
from app.util.logger import logger


class BaseCrawler:

    def __init__(self):
        logger.info('BaseCrawler.__init__')
        self.tempo_inicial = 0

    def crawl(self):
        """Inicializa a busca de informações no site"""
        logger.info('Método não implementado')
        pass

    def print_tempo_decorrido(self, tempo_inicial):
        tempo_decorrido = int(time.time() - tempo_inicial)
        segundos = tempo_decorrido % 60
        minutos = int(tempo_decorrido / 60) % 60
        horas = int(tempo_decorrido / (60*60)) % 60
        dias = int(tempo_decorrido / (60*60*24)) % 24

        if dias > 0:
            logger.info('Tempo decorrido: {} dias {} horas e {} minutos'.format(dias, horas, minutos))
        else:
            logger.info('Tempo decorrido: {} horas {} minutos e {} segundos'.format(horas, minutos, segundos))

    def print_tempo_medio_por_carta(self, tempo_inicial, indice_atual):
        tempo_decorrido = time.time() - tempo_inicial
        tempo_medio_segundos = int(tempo_decorrido / indice_atual)
        logger.info('Tempo médio por carta: {} segundos'.format(tempo_medio_segundos))
