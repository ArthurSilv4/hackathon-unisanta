import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# Inicializa o driver do Chrome
driver = webdriver.Chrome() 

# URL do site
url = "https://www.sympla.com.br/eventos/santos-sp" 

# Acessa a página
driver.get(url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="CustomGridstyle__CustomGridCardType-sc-1ce1n9e-2 jMNblV"]//a[@class="EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card"]')))
    
# Localiza o elemento do evento
evento = driver.find_element(
        By.XPATH,
    '//div[@class="CustomGridstyle__CustomGridCardType-sc-1ce1n9e-2 jMNblV"]//a[@class="EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card"]'
)
    
# Clica no evento
evento.click()
time.sleep(5) 

# Coleta o conteúdo HTML da nova página
element = driver.find_element(By.XPATH, '//section[@class="sc-b281498b-0 jQVtEv"] | //section[@class="sc-b281498b-0 ilWENo"]')
html_content = element.get_attribute('outerHTML')

print(html_content)

driver.quit()