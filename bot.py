import os, sys
from datetime import datetime

from botcity.web import WebBot, Browser, By
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt

from jogos.jogos import lista_jogos as jogos
from precos.precos import precos_historicos


# WebScraping
def navegar_precos(bot:WebBot):
    dados_extraidos = []
    for jogo in jogos:
        bot.browse(jogo["link"])
        bot.wait(2000)
        dados_jogo = extrair_dados(bot)

        dados_extraidos.append(dados_jogo)
    
    return dados_extraidos


def extrair_dados(bot:WebBot):
    # Título
    # //*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/h1
    # preço
    # //*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/label/div/span[1]/span/span[1]
    titulo = bot.find_element('//*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div/div/h1', By.XPATH).text
    preco = bot.find_element('//*[@id="main"]/div/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/label/div/span[1]/span/span[1]', By.XPATH).text
    preco = str(preco)
    preco = float(preco.replace("R$", "").replace(",","."))
    data = datetime.today()
    data = data.strftime("%d/%m/%Y")

    print(titulo, preco, data)
    bot.wait(1000)

    return {"Jogo" : titulo, "Valor" : preco, "Data" : data}


# Manipulação de dados
def criar_planilha(nomeArquivo):
    if not os.path.exists(nomeArquivo):
        colunas = ['Jogo', 'Valor', 'Data']
        df = pd.DataFrame(columns=colunas)
        df.to_excel(nomeArquivo, index =False, engine='openpyxl')
       
        print(f'Arquivo {nomeArquivo} criado!')
    else:
        print('Arquivo já existe')


def inserir_dados(nomeArquivo:str, dados_extraidos:list):
    dados = precos_historicos()
    
    for dado in dados:
        nome = str(dado["name"]).replace('â„¢','™')
        dados_tratados = tratar_dados(dado)
        popular_planilha(nome, dados_tratados, nomeArquivo)

    inserir_dados_extraidos(nomeArquivo, dados_extraidos)


def tratar_dados(json):
    dados = []
    for precos in json["data"]:
        valor = precos["y"]
        dia = precos["x"]["d"]
        mes = precos["x"]["m"] + 1
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
    print(f"Dados históricos do jogo {jogo} salvos no arquivo {caminho}")


def inserir_dados_extraidos(caminho:str, dados_extraidos:list):    
    planilha = pd.read_excel(caminho, engine='openpyxl')

    for dado in dados_extraidos:
        nova_linha = pd.DataFrame([{
            "Jogo" : dado["Jogo"],
            "Valor" : dado["Valor"],
            "Data" : dado["Data"]
         }])
        
        planilha = pd.concat([planilha, nova_linha], ignore_index=True)

    planilha.to_excel(caminho, index=False, engine='openpyxl')
    print(f'Dados extraídos salvos no arquivo {caminho}')


def criarGrafico(df: pd.DataFrame):
    # Recupera os valores únicos na coluna "PRODUTO" do DataFrame
    jogos = df["Jogo"].unique()
    
    # Itera a lista de produtos únicos e cria
    # um gráfico de linha para cada produto
    for jogo in jogos:
        # Filtra o DataFrame para obter apenas as linhas
        # onde o produto é igual ao produto da iteração
        dadosJogo = df[df['Jogo'] == jogo]
    
        # Plota e configura o gráfico de variação do preço
        plt.figure(figsize=(8, 5))
        plt.plot(dadosJogo['Data'], dadosJogo['Valor'], marker='o')
        plt.plot()

        plt.title(f'Variação de Preço: {jogo}', fontsize=10)
        plt.xlabel('Data')
        plt.ylabel('Preço (R$)')
        plt.xticks(rotation=45)
        
        # Mostra o gráfico
        plt.tight_layout()
        plt.show()


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
        nomeArquivo = 'planilha\planilha.xlsx'
        dados_extraidos = navegar_precos(bot)
        criar_planilha(nomeArquivo)
        inserir_dados(nomeArquivo, dados_extraidos)
        df = pd.read_excel(nomeArquivo, engine='openpyxl')
        criarGrafico(df)

    except Exception as ex:
        print(ex)
    
    finally:
        bot.wait(1000)
        bot.stop_browser()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
