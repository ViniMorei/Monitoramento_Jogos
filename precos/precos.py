import json

caminhos = [
    r'precos\DARKSOULSIII.json',
    r'precos\HORIZON.json',
    r'precos\RE4.json'
]

def precos_historicos():
    dados = []
    for caminho in caminhos:
        with open(caminho, 'r') as arquivo:
            dado = json.load(arquivo)
            dados.append(dado)

    return dados