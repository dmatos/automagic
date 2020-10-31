
from app.util.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def aplicar_filtro_de_pesquisa(driver):

    botao_de_filtro = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'button--toggle-filters')))
    botao_de_filtro.click()

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'Magic:TheGathering-filter')))
    except TimeoutException as ex:
        logger.exception(ex)
        fechar_filtro = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'button--dismiss')))
        fechar_filtro.click()
        return False

    checkbox_pai = driver.find_elements(By.CLASS_NAME, "search-filter__facet")

    for checkbox_filho in checkbox_pai:

        if 'Magic: The Gathering' in checkbox_filho.text:
            checkbox = checkbox_filho
            checkbox.click()
            break

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'Cards-filter')))

    #checkbox = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/section/div[1]/div[2]/div[2]/div[3]/div/span[1]/label/span[1]")
    #checkbox.click()

    fechar_filtro = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'button--dismiss')))
    fechar_filtro.click()

    return True
