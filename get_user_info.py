import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

#Parametros do Script
FILE_NAME = 'user_info.parquet' #Nome do Arquivo de Exportação
FILE_PATH = 'C:/Users/d.takeshi/Documents/workspace/apmt/' #Diretório de Expotação

#Inicializando Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.maximize_window()

df = pd.read_parquet('user_links.parquet')

result = []

for index, row in df.iterrows():

    #Lendo html da Página
    URL = row['links'] #'https://apmt.org.br/missionario/ageirson-corjesus-ramos/'

    #Requisição da Página Inicial
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    #Lendo os elementos necessários
    try:
        info = soup.find("div", {"class": "elementor-text-editor elementor-clearfix"})
        image = soup.find("img", {"class": "attachment-full size-full"})['src']
        letter = soup.find("a", {"class": "elementor-post__thumbnail__link"})['href']
        letter_tag = soup.find("div", {"class": "elementor-post__badge"}).text
    except:
        print('Sem carta!')

    nome, campo_missionario, conjuge, email, filho, endereco, codigo = '', '', '', '', '', '', ''

    for i in info:
        if i.name in ('h3', 'p'):
            if i.name == 'h3':
                nome = i.text
            elif i.text.find('Campo Missionário:') >= 0:
                campo_missionario = i.text
            elif i.text.find('Espos') >= 0:
                conjuge = i.text
            elif i.text.find('Email') >= 0:
                email = i.text
            elif i.text.find('Filh') >= 0:
                filho = i.text
            elif i.text.find('Endereço') >= 0:
                endereco = i.text
            elif i.text.find('Código para contribuição') >= 0:
                codigo = i.text

    print(f'informações coletadas: {nome},{campo_missionario},{conjuge},{email},{filho},{endereco},{codigo}')

    result.append([
        nome,
        campo_missionario,
        conjuge,
        email,
        filho,
        endereco,
        codigo,
        image,
        letter,
        letter_tag
    ])

print(result)

#Transformando em um Dataframe do Pandas
df = pd.DataFrame(result, columns = [
    'nome',
    'campo_missionario',
    'conjuge',
    'email',
    'filho',
    'endereco',
    'codigo',
    'image',
    'letter',
    'letter_tag'
    ])

#Exportando como CSV
df.to_parquet(FILE_PATH + FILE_NAME)

driver.quit()
