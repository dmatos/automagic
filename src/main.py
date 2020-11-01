# coding=utf8

import multiprocessing

from app.crawler.tcgplayer import TCGCrawler
from app.service import ListaCartasService

if __name__ == '__main__':
    # lista de cartas
    listaCartasService = ListaCartasService()
    lista_de_cartas = listaCartasService.buscar_cartas_scryfall()
    num_total_cartas = len(lista_de_cartas)
    # numero de threads disponíveis
    num_threads = multiprocessing.cpu_count()
    cartas_por_thread = int(num_total_cartas / num_threads)

    slice_start = 0
    threads = []
    for i in range(0, num_threads):
        sub_lista = lista_de_cartas[slice_start:slice_start+cartas_por_thread]
        slice_start += cartas_por_thread
        crawler = TCGCrawler(sub_lista)
        threads.append(crawler)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


