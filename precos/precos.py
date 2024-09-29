import json

caminhos = [
    r'precos\json\DARKSOULSIII.json',
    r'precos\json\HORIZON.json',
    r'precos\json\RE4.json'
]

def precos_historicos():
    dados = []
    for caminho in caminhos:
        with open(caminho, 'r') as arquivo:
            dado = json.load(arquivo)
            dados.extend(dado)

    return dados