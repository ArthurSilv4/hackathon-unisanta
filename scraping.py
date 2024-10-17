import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from anticaptchaofficial.recaptchav2proxyless import *
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

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

time.sleep(10)
# Clica no evento
evento.click()

# Coleta a nova URL
new_url = driver.current_url


# Resolver reCAPTCHA v2 (exemplo com 2Captcha)
solver = recaptchaV2Proxyless()
solver.set_verbose(1) 

# Obtém a API key e website key das variáveis de ambiente
api_key = os.getenv('API_KEY')
website_key = os.getenv('WEBSITE_KEY')

# Usa a API key no solver
solver.set_key(api_key)
solver.set_website_url(new_url)
solver.set_website_key(website_key)
solver.set_soft_id(0)

g_response = solver.solve_and_return_solution()
time.sleep(5) 

if g_response != 0:
    print(g_response)
else:
    print(solver.error_code)
    time.sleep(5) 


# Coleta o conteúdo HTML da nova página
element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//section[@class="sc-b281498b-0 jQVtEv"] | //section[@class="sc-b281498b-0 ilWENo"]'))
)
html_content = element.get_attribute('outerHTML')
print(html_content)
    
driver.quit()