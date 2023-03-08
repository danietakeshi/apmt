from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#Parametros do Script
FILE_NAME = 'user_letter.parquet' #Nome do Arquivo de Exportação
FILE_PATH = 'C:/Users/d.takeshi/Documents/workspace/apmt/' #Diretório de Expotação

#Inicializando Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.maximize_window()

df = pd.read_parquet('user_info.parquet')

result = []

for index, row in df.iterrows():
    if row['letter_tag'] == 'Cartas de Missionários' and index not in (37, 38, 63, 80, 86, 107, 134, 163):
        print(f'{index}, {row["nome"]},{row["letter"]}')

    #Lendo html da Página
    URL = row["letter"] #'https://apmt.org.br/rev-p-o-c-e-m-5/'

    #Requisição da Página Inicial
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    content = soup.find_all("div", {"class": "elementor-widget-container"})

    full_text = ''

    for tag in content:
        for c in tag:
            if c.name in ('h3', 'p'):
                if c.text.find('Agência Presbiteriana de Missões Transculturais') < 0 or c.text.find('04.138.895/0001-86') < 0:
                    full_text = full_text + c.text + '\n'

    result.append([
        row["nome"],
        row["letter"],
        full_text
    ])

print(result)

#Transformando em um Dataframe do Pandas
df = pd.DataFrame(result, columns = [
    'nome',
    'letter',
    'full_text'
    ])

#Exportando como CSV
df.to_parquet(FILE_PATH + FILE_NAME)

driver.quit()
