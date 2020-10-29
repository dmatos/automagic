# coding=utf8

from app.util.logger import logger
from app.tools import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from aplicar_filtro_de_pesquisa import *
from paginas_count import *
from capturar_links_em_todas_paginas import *
from buscar_banco_de_cartas import *

if __name__=='__main__':


    driver = chrome_driver.inicializar_driver('resources/downloads', headless=False)

    lista_de_cartas = buscar_banco_de_cartas()

    #logger.info("Tipo: {}".format(type(lista_de_cartas)))
    logger.info("{}".format(lista_de_cartas['data']))


    for carta in lista_de_cartas['data']:
        driver.get('https://www.tcgplayer.com/')
        barra_de_busca = driver.find_element(By.TAG_NAME, 'input')

        if carta.find('/') != -1:
            carta = carta[ :carta.find('/')]
        else:
            pass

        carta_procurada = carta
        barra_de_busca.send_keys(carta_procurada)
        botao_buscar = driver.find_element(By.CLASS_NAME, 'search-bar__spyglass')
        botao_buscar.click()

        aplicar_filtro_de_pesquisa(driver)

        time.sleep(1)

        quantidade_de_paginas = paginas_count(driver)

        lista_de_links = capturar_links_em_todas_paginas(driver, quantidade_de_paginas)

        for link in lista_de_links:
            driver.get(link)
            #TODO CAPTURAR INFORMAÇÕES DA CARTA

            card_name = driver.find_element(By.XPATH, "/html/body/div[4]/section[1]/div/section/div[3]/div[1]/h1")
            edition = driver.find_element(By.XPATH, "/html/body/div[4]/section[1]/div/section/div[3]/div[1]/div/a")
            market_price = driver.find_element(By.CLASS_NAME, 'price-point__data')

            time.sleep(1)


            detalhes_do_produto = driver.find_element(By.CLASS_NAME, "product-details__actions")
            detalhes_de_preco = detalhes_do_produto.find_element(By.CLASS_NAME, "product-details__listing-count")
            total_prices = detalhes_de_preco.find_element(By.CLASS_NAME, "product-details__listing-count-header")
            rarity = driver.find_element(By.XPATH, "/html/body/div[4]/section[1]/div/section/div[3]/table/tbody/tr/td/dl/dd[1]")


            logger.info("/////////////////////////////////////////////////////////////")
            logger.info("Card Name: {}".format(card_name.text))
            logger.info("Edition: {}".format(edition.text))
            logger.info("Rarity, #: {}".format(rarity.text))
            logger.info("Total Prices: {}".format(total_prices.text))
            logger.info("Market Price: {}".format(market_price.text))
            logger.info("                                                                 ")
            #input("tecle ENTER para continuar")


            #TODO FUNCAO PARA CASOS ONDE EXISTE MAIS DE UMA PAGINA DE OFERTAS DA MESMA CARTA
            if len(total_prices.text) > 0:
                tabela_de_precos = driver.find_element(By.CLASS_NAME, "priceTableWrapper")

                lista_de_lojas = tabela_de_precos.find_elements(By.CLASS_NAME, "product-listing")

                for loja in lista_de_lojas:

                    nome_da_loja = loja.find_element(By.CLASS_NAME, "seller__name")
                    preco = loja.find_element(By.CLASS_NAME, "product-listing__price")
                    estoque = loja.find_element(By.CLASS_NAME, "product-listing__qty-available")
                    conservacao = loja.find_element(By.CLASS_NAME, "product-listing__condition")

                    logger.info("nome da loja: {}".format(nome_da_loja.text))
                    logger.info("preço: {}".format(preco.text))
                    logger.info("estoque: 1 {}".format(estoque.text))
                    logger.info("estado de conservação: {}".format(conservacao.text))
                    logger.info("------------------------------------------------------------------")




                #input("tecle ENTER para terminar")
            else:
                pass


    driver.quit()

