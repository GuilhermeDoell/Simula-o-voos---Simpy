# Desafio Lista de Voos

## Descrição
Este script realiza a simulação, por meio de variáveis, trazendo a probabilidade de um passageiro comparecer no terminal apresentando as estatísticas da quantidade de passageiros atendidos e negados e a taxa de atendimento, a partir dos voos listados no arquivo xlsx.

## Requisitos

Para que seja possível executar o script com o streamlit, primeiro é necessário abrir o terminal e criar um ambiente virtual através do comando abaixo: 

> python -m venv env

E ativar o ambiente virtual criado com o comando:

Mac ou Linux:
> source env/bin/activate  

Windows:
> source env/Scripts/activate

Instalar as seguintes dependências:

> pip install simpy streamlit pandas openpyxl random numpy

Por fim, executar o streamlit com comando:

> streamlit run app.py
