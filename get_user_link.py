
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

#Parametros do Script
URL = "https://apmt.org.br/missionarios/" #URL de busca
FILE_NAME = 'user_links.parquet' #Nome do Arquivo de Exportação
FILE_PATH = 'C:/Users/d.takeshi/Documents/workspace/apmt/' #Diretório de Expotação

#Inicializando Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.maximize_window()

#Requisição da Página Inicial
driver.get(URL)

results = []

soup = BeautifulSoup(driver.page_source, "html.parser")

links = soup.find_all("a", {"class": "elementor-post__thumbnail__link"})

for link in links:
    print(link['href'])
    results.append([link['href']])

#Transformando em um Dataframe do Pandas
df = pd.DataFrame(results, columns = ['links'])

#Exportando como CSV
df.to_parquet(FILE_PATH + FILE_NAME)

driver.quit()
