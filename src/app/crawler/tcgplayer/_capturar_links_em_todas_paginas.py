from app.util.logger import logger
from app.tools import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def capturar_links_em_todas_paginas(driver, quantidade_de_paginas):

    lista_de_links = []
    pagina = 1

    while pagina <= quantidade_de_paginas:

        logger.info("Pag {}".format(pagina))

        #time.sleep(1)

        pagina_de_resultados = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-results')))
        resultados = pagina_de_resultados.find_elements(By.CLASS_NAME, 'search-result')

        for carta in resultados:

            atag = carta.find_element(By.TAG_NAME, 'a')
            link = atag.get_attribute('href')
            lista_de_links.append(link)

        if pagina < quantidade_de_paginas:
            proxima_pagina = driver.find_element(By.ID, "nextButton")
            proxima_pagina.click()
        else:
            pass
        pagina = pagina + 1

    return lista_de_links