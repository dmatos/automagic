
from app.util.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def aplicar_filtro_de_pesquisa(driver):

    botao_de_filtro = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/div/div[1]/button/span")
    botao_de_filtro.click()

    WebDriverWait(driver, 15).until(
       EC.presence_of_element_located((By.ID, 'Magic:TheGathering-filter')))

    checkbox_pai = driver.find_elements(By.CLASS_NAME, "search-filter__facet")

    for checkbox_filho in checkbox_pai:

        if 'Magic: The Gathering' in checkbox_filho.text :
            checkbox = checkbox_filho
            checkbox.click()
            break

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'Cards-filter')))
    checkbox = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/section/div[1]/div[2]/div[2]/div[3]/div/span[1]/label/span[1]")
    checkbox.click()

    fechar_filtro = driver.find_element(By.XPATH, "/html/body/div[1]/div/section[2]/section/div[1]/div[3]/button[2]")
    fechar_filtro.click()