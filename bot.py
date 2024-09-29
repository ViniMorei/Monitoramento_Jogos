import os

from botcity.web import WebBot, Browser, By
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import openpyxl

from jogos.jogos import lista_jogos as jogos
from precos.precos import precos_historicos


# WebScraping
def navegar_precos(bot:WebBot):
    for jogo in jogos:
        bot.browse(jogo["link"])
        bot.wait(2000)
        extrair_dados(bot)

def extrair_dados(bot:WebBot):
    # Título
    # //*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/h1
    # preço
    # //*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/label/div/span[1]/span/span[1]
    titulo = bot.find_element('//*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/h1', By.XPATH).text
    preco = bot.find_element('//*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/label/div/span[1]/span/span[1]', By.XPATH).text

    print(titulo, preco)
    bot.wait(1000)


# Manipulação de dados
def criar_planilha(nomeArquivo):
    if not os.path.exists(nomeArquivo):
        colunas = ['Jogo', 'Valor', 'Data']
        df = pd.DataFrame(columns=colunas)
        df.to_excel(nomeArquivo, index =False, engine='openpyxl')
       
        print(f'Arquivo {nomeArquivo} criado!')
    else:
        print('Arquivo já existe')


def navegar_json(nomeArquivo):
    dados = precos_historicos()
    
    for dado in dados:
        nome = dado["name"]
        dados_tratados = tratar_dados(dado)
        popular_planilha(nome, dados_tratados, nomeArquivo)


def tratar_dados(json):
    dados = []
    for precos in json["data"]:
        valor = precos["y"]
        dia = precos["x"]["d"]
        mes = precos["x"]["m"]
        ano = precos["x"]["y"]
        data = f'{dia}/{mes}/{ano}'

        dados.append({"Valor" : valor, "Data" : data})

    return dados


def popular_planilha(jogo:str,dados:list, caminho:str):
    planilha = pd.read_excel(caminho, engine='openpyxl')

    for dado in dados:
        nova_linha = pd.DataFrame([{
            "Jogo" : jogo,
            "Valor" : dado["Valor"],
            "Data" : dado["Data"]
         }])
        
        planilha = pd.concat([planilha, nova_linha], ignore_index=True)

    planilha.to_excel(caminho, index=False, engine='openpyxl')
    print(f"Dados do jogo {jogo} salvos no arquivo {caminho}")


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    
    try:
        criar_planilha('planilha\planilha.xlsx')
        navegar_json()

    except Exception as ex:
        print(ex)
    
    finally:
        bot.wait(1000)
        bot.stop_browser()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
