# Monitoramento de Preços de Jogos

Esta automação realiza _webscraping_ para recuperar dados de preços de jogos de _PlayStation 4_ e ao final da execução adiciona esses dados numa planilha e cria gráficos de variação de preço ao longo do tempo 

## Início

Estas instruções detalham o fluxo que deve ser seguido para poder executar esta automação

### Pré-requisitos
- Ter o Python instalado na máquina
- Ter o Anaconda Navigator instalado para gerenciamento de ambientes e dependências


### Execução
- Realizar um _clone_ do projeto
  ```
  git clone https://github.com/ViniMorei/Monitoramento_Jogos.git
  ```

- Criar um ambiente Conda. Dentro da pasta do projeto, rodar esse código
    ```
    conda create --name Monitoramento_Jogos python=3.10
    conda activate Monitoramento_Jogos
    ```

- Testar
    ```
    python --version
    >>> Python 3.10.4
    ```   

- Instalar as dependências

    ```
    pip install -r requirements.txt
    ```   

- Executar o bot
    ```
    python bot.py
    ```