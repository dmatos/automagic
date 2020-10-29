from selenium.webdriver.common.by import By

def paginas_count(driver):
    result_count = driver.find_element(By.CLASS_NAME, "search-result-count")
    separador1 = result_count.text.split()
    separador2 = separador1[0]
    numero_de_paginas = int(separador2)/24

    if numero_de_paginas < 1:
        numero_de_paginas = 1
    else:
        pass

    return int(numero_de_paginas)