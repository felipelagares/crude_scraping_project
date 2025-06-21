import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

months = {
    1:'Janeiro',
    2:'Fevereiro',
    3:'Março',
    4:'Abril',
    5:'Maio',
    6:'Junho',
    7:'Julho',
    8:'Agosto',
    9:'Setembro',
    10:'Outubro',
    11:'Novembro',
    12:'Dezembro'
}

def scrape_links(current_date: datetime, driver: webdriver.Chrome):
    
    url = f'https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados?ano={current_date.year}&mes={months[current_date.month]}'
    driver.get(url)
    time.sleep(1)
    xpath = '/html/body/div[1]/div/main/div[1]/div/div[2]/div/div/div/div[2]/section/div/div[2]/div/div[2]/div/ul/li[1]/a'
    element = driver.find_elements(By.XPATH, xpath)
    if element:
        link = element[0].get_attribute('href')
        filename = element[0].text
        print(f"Link encontrado: url='{link}', nome='{filename}'")
        # Salva o link no arquivo txt, sempre adicionando uma nova linha
        with open('links_encontrados.txt', 'a', encoding='utf-8') as f:
            f.write(f"{link}\n")


def att_month(current_date: datetime):
    # Retorna o próximo mês
    if current_date.month == 12:
        return datetime(current_date.year + 1, 1, 1)
    else:
        return datetime(current_date.year, current_date.month + 1, 1)
    

if __name__ == "__main__":
    init = datetime(2002, 1, 1)
    end = datetime.now()
    current_date = init

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)

    while current_date <= end:
        scrape_links(current_date, driver)
        current_date = att_month(current_date)

    
    driver.quit()