# coding=utf8

from app.util.logger import logger
from app.tools import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__=='__main__':
    driver = chrome_driver.inicializar_driver('resources/downloads', headless=False)
    driver.get('https://www.tcgplayer.com/')
    barra_de_busca = driver.find_element(By.TAG_NAME, 'input')
    #logger.info(barra_de_busca.get_attribute('innerHTML'))

    barra_de_busca.send_keys('Mana Crypt')
    botao_buscar = driver.find_element(By.CLASS_NAME, 'search-bar__spyglass')
    botao_buscar.click()

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
        preco = 10
        logger.info("preço da carta: {}".format(preco))
        input("tecle ENTER para continuar")


    input("tecle ENTER para terminar")
    driver.quit()