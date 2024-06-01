import random
import streamlit as st
import numpy as np
import simpy
from flights import voos_df

def simular(media_pax_dia, media_atendimento, num_atendentes, num_dias):
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
                yield env.timeout(random.gauss(media_atendimento, 1))
                stats.tempo_ocupado += env.now - inicio_atendimento
            else:
                stats.pass_negados += 1

    def chegada_passageiros(env, terminal, atendentes, voos_df, stats):
        while True:
            for index, voo in voos_df.iterrows():
                num_passageiros = int(np.random.normal(media_pax_dia, 2))
                for i in range(num_passageiros):
                    env.process(passageiro(env, f'PAX_{index}_{i}', terminal, atendentes, stats))
                yield env.timeout(24)

    env = simpy.Environment()
    terminal = simpy.Resource(env, capacity=num_atendentes)
    env.process(chegada_passageiros(env, terminal, terminal, voos_df, stats))
    env.run(until=num_dias * 24)

    return stats.pass_atendidos, stats.pass_negados, stats.tempo_ocupado / (num_atendentes * num_dias * 24) * 100

st.title("Simulação de Atendimento no Terminal")

media_pax_dia = st.slider("Média de Passageiros por Dia", 1, 20, 10)
media_atendimento = st.slider("Média de Tempo de Atendimento (horas)", 1, 5, 3)
num_atendentes = st.slider("Número de Atendentes", 1, 10, 3)
num_dias = st.slider("Número de Dias de Simulação", 10, 200, 100)

if st.button("Iniciar Simulação"):
    pass_atendidos, pass_negados, taxa_utilizacao = simular(media_pax_dia, media_atendimento, num_atendentes, num_dias)
    st.write(f"Passageiros Atendidos: {pass_atendidos}")
    st.write(f"Passageiros Negados: {pass_negados}")
    st.write(f"Taxa de Utilização dos Atendentes: {taxa_utilizacao:.2f}%")