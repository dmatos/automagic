# coding=utf8

#system
import time
#3d
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
#project
from app.crawler import BaseCrawler
from ._capturar_links_em_todas_paginas import capturar_links_em_todas_paginas
from app.service import ListaCartasService
from app.util import logger
from app.tools import ChromeDriver


class TCGCrawler(BaseCrawler):

    def __init__(self, lista_de_cartas):
        super().__init__()
        logger.info('Inicializando TCGCrawler')
        self.driver = None
        self.url = 'https://www.tcgplayer.com/'
        self.query_string = 'search/magic/product?productLineName=magic&q='
        self.tempo_inicial = time.time()
        self.lista_de_cartas = lista_de_cartas

    def _paginas_count(self, driver):
        """Conta o número de páginas do resultado"""
        result_count = driver.find_element(By.CLASS_NAME, "search-result-count")
        separador1 = result_count.text.split()
        separador2 = separador1[0]
        numero_de_paginas = int(separador2)/24
        if numero_de_paginas < 1:
            numero_de_paginas = 1
        else:
            pass
        return int(numero_de_paginas)

    def _raspar_lojas(self, driver):
        total_prices_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "totalPrices")))
        total_prices_data = ''
        count_sencods, max_seconds = 0, 10
        while len(total_prices_data) == 0 and count_sencods < max_seconds:
            total_prices_data = total_prices_el.get_attribute('innerHTML')
            time.sleep(1)
            count_sencods += 1
        logger.info("Total Prices: {}".format(total_prices_data))
        tabela_de_precos = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "priceTableWrapper")))
        try:
            #TODO raspar as demais paǵinas de lojas, quando houver
            lista_de_lojas = tabela_de_precos.find_elements(By.CLASS_NAME, "product-listing")

            for loja in lista_de_lojas:

                nome_da_loja_el = loja.find_element(By.CLASS_NAME, "seller__name")
                nome_da_loja_data = nome_da_loja_el.get_attribute('innerHTML')
                preco_el = loja.find_element(By.CLASS_NAME, "product-listing__price")
                preco_data = preco_el.get_attribute('innerHTML')
                estoque_el = loja.find_element(By.CLASS_NAME, "product-listing__qty-available")
                estoque_data = estoque_el.get_attribute('innerHTML')
                conservacao_el = loja.find_element(By.CLASS_NAME, "product-listing__condition")
                conservacao_data = conservacao_el.find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')

                logger.info("nome da loja: {}".format(nome_da_loja_data))
                logger.info("preço: {}".format(preco_data))
                logger.info("estoque: 1 {}".format(estoque_data))
                logger.info("estado de conservação: {}".format(conservacao_data))
                logger.info("------------------------------------------------------------------")
                #input("tecle ENTER para terminar")
        except NoSuchElementException as ex:
            logger.exception(ex)
            pass
        except StaleElementReferenceException as ex:
            logger.exception(ex)
            pass

    def _raspar_dados_carta(self, driver, link):
        driver.get(link)
        card_name_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-details__name')))
        card_name_data = card_name_el.get_attribute('innerHTML')
        edition_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-details__set')))
        edition_data = edition_el.find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')
        market_price_el = driver.find_element(By.CLASS_NAME, 'price-point__data')
        market_price_data = market_price_el.get_attribute('innerHTML')
        table_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'table')))
        term_els = table_el.find_elements(By.CLASS_NAME, 'product-description__term')
        value_els = table_el.find_elements(By.CLASS_NAME, 'product-description__value')
        terms_values = {}

        index = 0
        while index < len(term_els):
            term_text = term_els[index].get_attribute('innerHTML')
            terms_values[term_text] = value_els[index].get_attribute('innerHTML')
            index += 1

        logger.info("/////////////////////////////////////////////////////////////")
        logger.info("Card Name: {}".format(card_name_data))
        logger.info("Edition: {}".format(edition_data))

        for key in terms_values.keys():
            logger.info('{} {}'.format(key, terms_values[key]))
        logger.info("Market Price: {}".format(market_price_data))
        logger.info("#############################################################")

        self._raspar_lojas(driver)

    def _raspar_cartas(self, esconder_navegador=True):
        chrome = ChromeDriver()
        driver = chrome.inicializar_driver('resources/downloads', headless=esconder_navegador)
        try:
            #logger.info("Tipo: {}".format(type(lista_de_cartas)))
            #logger.info("{}".format(lista_de_cartas))
            driver.get(self.url)

            num_de_cartas = len(self.lista_de_cartas)
            self.tempo_inical = time.time()

            for index in range(0, num_de_cartas):
                carta = self.lista_de_cartas[index]
                if carta.find('/') != -1:
                    # ignorar de / para frente no nome da cata
                    carta = carta[:carta.find('/')]
                self.print_tempo_decorrido(self.tempo_inical)
                self.print_tempo_medio_por_carta(self.tempo_inical, index+1)
                logger.info('Buscando ({}/{}): {}'.format(index+1, num_de_cartas, carta))
                url_busca = '{}{}{}'.format(self.url, self.query_string, carta)
                driver.get(url_busca)
                quantidade_de_paginas = self._paginas_count(driver)
                try:
                    lista_de_links = capturar_links_em_todas_paginas(driver, quantidade_de_paginas)
                    for link in lista_de_links:
                        self._raspar_dados_carta(driver, link)
                except TimeoutException as ex:
                    logger.exception(ex)
                    pass
        finally:
            if driver is not None:
                driver.quit()

    def run(self):
        self._raspar_cartas()
