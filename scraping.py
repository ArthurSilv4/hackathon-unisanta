import os
import time
import re
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import math

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o driver do Chrome
driver = webdriver.Chrome()

# URL do site
url = "https://www.sympla.com.br/eventos/santos-sp"

# Acessa a página
driver.get(url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="CustomGridstyle__CustomGridCardType-sc-1ce1n9e-2 jMNblV"]//a[@class="EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card"]')))

qtd_events = BeautifulSoup(driver.page_source, 'html.parser')
qtd_events = qtd_events.find('h2', class_='Searchstyle__SearchBodyTotalResult-sc-1yqauwc-5 cFHGiO').get_text().strip()

index = qtd_events.find(' ')
qtd_events = qtd_events[:index]

ultima_pagina = math.ceil(int(qtd_events)/20)

print(qtd_events)

data = []

for i in range(1, ultima_pagina + 1):
    # Formatar o XPath corretamente
    xpath = f'//div[@class="CustomGridstyle__CustomGridCardType-sc-1ce1n9e-2 jMNblV"]//a[@class="EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card" and @data-position="{i}"]'

    try:
        # Espera explícita para garantir que o elemento esteja presente
        evento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Fazer scroll até o elemento
        driver.execute_script("arguments[0].scrollIntoView();", evento)
        time.sleep(2)  # Espera para garantir que o scroll foi concluído

        # Clica no evento usando JavaScript
        driver.execute_script("arguments[0].click();", evento)

        # Coleta a nova URL
        new_url = driver.current_url

        # Resolver reCAPTCHA v2 (exemplo com 2Captcha)
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1) 

        # Obtém a API key e website key das variáveis de ambiente
        api_key = os.getenv('API_KEY')
        website_key = os.getenv('WEBSITE_KEY')

        #---------------------------------------------
        # Função para verificar se o CAPTCHA está presente
        def is_captcha_present(driver):
            try:
                driver.find_element(By.ID, 'captcha-element-id')
                return True
            except NoSuchElementException:
                return False

        # Verificar se o CAPTCHA está presente
        if is_captcha_present(driver):
            # Código para resolver o CAPTCHA
            solver.set_key(api_key)
            solver.set_website_url(driver.current_url)
            solver.set_website_key(website_key)
            solver.set_soft_id(0)

            g_response = solver.solve_and_return_solution()
            time.sleep(5)

            if g_response != 0:
                print(g_response)
                # Inserir a resposta do CAPTCHA no campo apropriado
                captcha_response_field = driver.find_element(By.ID, 'captcha-element-id')
                captcha_response_field.send_keys(g_response)
            else:
                print(solver.error_code)
                time.sleep(5)
        else:
            print("CAPTCHA não está presente na página.")
        #---------------------------------------------

        # Coleta o conteúdo HTML da nova página
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//section[@class="sc-b281498b-0 jQVtEv"]'))
        )

        element2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//section[@class="sc-b281498b-0 ilWENo"]'))
        )

        html_content = element.get_attribute('outerHTML')
        html_content2 = element2.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')
        title_text = soup.find('h1').get_text() if soup.find('h1') else 'H1 não encontrado'

        date_text = soup.find('div', class_='sc-983ba91-1 cZLMzD')
        date_text = date_text.get_text() if date_text else 'Data não encontrada'

        value_text = soup.find('div', class_='sc-28aed0db-2 kUkoAR')
        value_text = value_text.get_text() if value_text else 'Valor não encontrado'

        location_text = soup.find('div', class_='sc-983ba91-2 sc-983ba91-3 leDNYU')
        location_text = location_text.get_text() if location_text else 'Localização não encontrada'

        purchase_link = new_url
        validate_link = new_url

        if html_content2:
            soup2 = BeautifulSoup(html_content2, 'html.parser')

            # Encontra as duas divs que contêm os elementos p
            divs = soup2.find_all('div', class_='sc-575bb398-0 emgExH')

            # Extrai o texto de todos os elementos p dentro das divs
            p_texts = [p.get_text() for div in divs for p in div.find_all('p')]

            # Junta os textos dos elementos p em uma única string
            description_text = ' '.join(p_texts) if p_texts else 'P não encontrado'
        else:
            description_text = 'HTML content2 não encontrado'

        # Função para normalizar e decodificar sequências de escape Unicode
        def normalize_unicode(text):
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

        # Função para extrair apenas o número de uma string
        def extract_number(text):
            match = re.search(r'\d+,\d+', text)
            return match.group() if match else '0,00'

        # Normaliza e decodifica sequências de escape Unicode
        title_text = normalize_unicode(title_text)
        date_text = normalize_unicode(date_text)
        value_text = normalize_unicode(value_text)
        location_text = normalize_unicode(location_text)
        description_text = normalize_unicode(description_text)

        # Extrair apenas o número do valor
        value_text = extract_number(value_text)

        # Adicionar os dados ao array
        data.append({
            'title': title_text,
            'date': date_text,
            'value': value_text,
            'location': location_text,
            'description': description_text,
            'purchase_link': purchase_link,
            'validate_link': validate_link
        })

        time.sleep(5)
        # Volta para a página anterior
        driver.back()

    except Exception as e:
        print(f"Erro ao processar o evento na posição {i}: {e}")

# Converte a lista de dicionários para um DataFrame
data_df = pd.DataFrame(data)

# Converte o DataFrame para uma lista de dicionários
data_dict = data_df.to_dict('records')

driver.quit()

# Salva os dados em um arquivo JSON
js = json.dumps(data_dict)
with open('data.json', 'w') as fp:
    fp.write(js)