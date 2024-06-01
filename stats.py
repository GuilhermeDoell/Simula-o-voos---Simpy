import random
import numpy as np
import simpy
from simulation import MEDIA_ATENDIMENTO, MEDIA_PAX_DIA, NUM_ATENDENTES, NUM_DIAS
from flights import voos_df

class Estatisticas:
    def __init__(self):
        self.pass_atendidos = 0
        self.pass_negados = 0
        self.tempo_ocupado = 0

stats = Estatisticas()

def passageiro(env, nome, terminal, atendentes, stats):
    chegada = env.now
    with atendentes.request() as req:
        resultado = yield req | env.timeout(0)
        if req in resultado:
            stats.pass_atendidos += 1
            inicio_atendimento = env.now
            yield env.timeout(random.gauss(MEDIA_ATENDIMENTO, 1))
            stats.tempo_ocupado += env.now - inicio_atendimento
        else:
            stats.pass_negados += 1

def chegada_passageiros(env, terminal, atendentes, voos_df, stats):
    while True:
        for index, voo in voos_df.iterrows():
            num_passageiros = int(np.random.normal(MEDIA_PAX_DIA, 2))
            for i in range(num_passageiros):
                env.process(passageiro(env, f'PAX_{index}_{i}', terminal, atendentes, stats))
            yield env.timeout(24)

env = simpy.Environment()
terminal = simpy.Resource(env, capacity=NUM_ATENDENTES)
env.process(chegada_passageiros(env, terminal, terminal, voos_df, stats))
env.run(until=NUM_DIAS * 24)

# Estatísticas finais
print(f'Passageiros atendidos: {stats.pass_atendidos}')
print(f'Passageiros negados: {stats.pass_negados}')
print(f'Taxa de utilização dos agentes: {stats.tempo_ocupado / (NUM_ATENDENTES * NUM_DIAS * 24) * 100:.2f}%')