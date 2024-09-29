import json
import requests
from bs4 import BeautifulSoup

from botcity.web import WebBot, Browser, By
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from webdriver_manager.chrome import ChromeDriverManager

from jogos.jogos import lista_jogos as jogos
from precos.precos import precos_historicos

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


def navegar_json():
    dados = precos_historicos()
    
    dadosre4 = dados[2]
    dadostratados = tratar_dados(dadosre4)
    print(dadostratados)

    # for precos in dados:
    #     print(precos["name"])


def tratar_dados(dummy):
    dados = []
    for precos in dummy["data"]:
        valor = precos["y"]
        dia = precos["x"]["d"]
        mes = precos["x"]["m"]
        ano = precos["x"]["y"]
        data = f'{dia}/{mes}/{ano}'

        dados.append({"Valor" : valor, "Data" : data})

    return dados


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
