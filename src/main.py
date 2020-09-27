# coding=utf8

from app.util.logger import logger
from app.tools import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

if __name__=='__main__':
    driver = chrome_driver.inicializar_driver('resources/downloads', headless=False)
    driver.get('https://www.tcgplayer.com/')
    barra_de_busca = driver.find_element(By.TAG_NAME, 'input')
    #logger.info(barra_de_busca.get_attribute('innerHTML'))

    carta_procurada = "Forest"
    barra_de_busca.send_keys(carta_procurada)
    botao_buscar = driver.find_element(By.CLASS_NAME, 'search-bar__spyglass')
    botao_buscar.click()

    botao_de_filtro = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/div/div[1]/button/span")
    botao_de_filtro.click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'Magic:TheGathering-filter')))
    checkbox = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/section/div[1]/div[2]/div[2]/div[1]/div/span[1]/label/span[2]")
    checkbox.click()
    fechar_filtro = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/section/div[1]/div[3]/button[2]")
    fechar_filtro.click()

    time.sleep(5)#TODO MELHORAR ESSA SOLUÇÃO (NÃO FUNCIONA SEM ESSE INTERVALO)

    pagina_de_resultados = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'search-results')))
    resultados = pagina_de_resultados.find_elements(By.CLASS_NAME, 'search-result')

    lista_de_links = []

    for carta in resultados:
        atag = carta.find_element(By.TAG_NAME, 'a')
        link = atag.get_attribute('href')
        lista_de_links.append(link)

    for link in lista_de_links:
        driver.get(link)
        #TODO CAPTURAR INFORMAÇÕES DA CARTA

        edition = driver.find_element(By.XPATH, '/html/body/div[5]/section[1]/div/section/div[3]/div[1]/div/a')
        market_price = driver.find_element(By.CLASS_NAME, 'price-point__data')
        #total_prices = driver.find_element(By.CLASS_NAME, "product-details__listing-count-header") NÃO ESTA FUNCIONANDO
        rarity = driver.find_element(By.XPATH, "/html/body/div[5]/section[1]/div/section/div[3]/table/tbody/tr/td/dl/dd[1]")

        logger.info("___________________________________________________")
        logger.info("Card Name: {}".format(carta_procurada))
        logger.info("Edition: {}".format(edition.text))
        logger.info("Rarity, #: {}".format(rarity.text))
        #logger.info("Total Prices: {}".format(total_prices.text))#NÃO FUNCIONA SEMPRE
        logger.info("Market Price: {}".format(market_price.text))
        logger.info("___________________________________________________")
        #input("tecle ENTER para continuar")


    #input("tecle ENTER para terminar")
    driver.quit()

