import simpy
import random
import numpy as np
from flights import voos_df

# Parâmetros
MEDIA_PAX_DIA = 10
MEDIA_ATENDIMENTO = 3  # horas
NUM_ATENDENTES = 3
NUM_DIAS = 100

# Função para simular um passageiro
def passageiro(env, nome, terminal, atendentes):
    chegada = env.now
    print(f'{nome} chegou ao terminal em {chegada:.2f}')
    with atendentes.request() as req:
        resultado = yield req | env.timeout(0)
        if req in resultado:
            print(f'{nome} está sendo atendido em {env.now:.2f}')
            yield env.timeout(random.gauss(MEDIA_ATENDIMENTO, 1))
            print(f'{nome} foi atendido em {env.now:.2f}')
        else:
            print(f'{nome} foi negado atendimento em {env.now:.2f}')

# Função para simular a chegada de passageiros
def chegada_passageiros(env, terminal, atendentes, voos_df):
    while True:
        for index, voo in voos_df.iterrows():
            # Distribuição normal para o número de passageiros que aparecem
            num_passageiros = int(np.random.normal(MEDIA_PAX_DIA, 2))
            for i in range(num_passageiros):
                env.process(passageiro(env, f'PAX_{index}_{i}', terminal, atendentes))
            yield env.timeout(24)  # Avança um dia

# Criar o ambiente de simulação
env = simpy.Environment()
terminal = simpy.Resource(env, capacity=NUM_ATENDENTES)
env.process(chegada_passageiros(env, terminal, terminal, voos_df))
env.run(until=NUM_DIAS * 24)  # Simula 100 dias