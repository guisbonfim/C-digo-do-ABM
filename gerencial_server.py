import numpy as np
from gerencial_a import Model  # Importação do modelo de simulação
import matplotlib.pyplot as plt  # Importação da biblioteca de plotagem
import pandas as pd  # Importação da biblioteca Pandas para manipulação de dados

plt.close('all')  # Fecha todas as figuras de plotagem anteriores, se houver

# Definição de uma função para calcular a média de uma lista de valores
def calcular_media(vetor):
    soma = sum(vetor)
    media = soma / len(vetor)
    return media

# Definição dos parâmetros para as simulações
simulacoes = 100 # Número de simulações
num_e_1 = 1  # Número de equipes tipo 1
num_t_1 = 10  # Número de trabalhadores por equipe tipo 1
num_e_2 = 1  # Número de equipes tipo 2
num_t_2 = 7  # Número de trabalhadores por equipe tipo 2
num_t_3 = 20  # Número de trabalhadores tipo 3
num_d = 900  # Número de dias de simulação

risco = 0.5  # Risco do canteiro
feedback = 0.7  # Frequência de feedback

# Listas para armazenar os resultados das simulações para diferentes configurações
gerencial_diario_bianual = []
gerencial_diario_anual = []
gerencial_diario_semestral = []
gerencial_diario_trimestral = []
gerencial_diario = []
gerencial_semanal_bianual = []
gerencial_semanal_anual = []
gerencial_semanal_semestral = []
gerencial_semanal_trimestral = []
gerencial_semanal = []
gerencial_bianual = []
gerencial_anual = []
gerencial_semestral = []
gerencial_trimestral = []

# Realização das simulações
# Realização das simulações
initial_perceived_workgroup_norm_a1 = []
initial_perceived_workgroup_norm_a2 = []
initial_perceived_workgroup_norm_a3 = []
initial_perceived_workgroup_norm_a = []
initial_perceived_workgroup_norm_b = []
initial_perceived_workgroup_norm_c = []
initial_perceived_workgroup_norm_d = []
initial_perceived_workgroup_norm_e = []
initial_perceived_workgroup_norm_f = []
initial_perceived_workgroup_norm_g = []
initial_perceived_workgroup_norm_h = []
initial_perceived_workgroup_norm_j = []
initial_perceived_workgroup_norm_k = []
initial_perceived_workgroup_norm_l = []

initial_perceived_management_norm_a1 = []
initial_perceived_management_norm_a2 = []
initial_perceived_management_norm_a3 = []
initial_perceived_management_norm_a = []
initial_perceived_management_norm_b = []
initial_perceived_management_norm_c = []
initial_perceived_management_norm_d = []
initial_perceived_management_norm_e = []
initial_perceived_management_norm_f = []
initial_perceived_management_norm_g = []
initial_perceived_management_norm_h = []
initial_perceived_management_norm_j = []
initial_perceived_management_norm_k = []
initial_perceived_management_norm_l = []

taxas_de_incidentes_a1 = []
taxas_de_incidentes_a2 = []
taxas_de_incidentes_a3 = []
taxas_de_incidentes_a = []
taxas_de_incidentes_b = []
taxas_de_incidentes_c = []
taxas_de_incidentes_d = []
taxas_de_incidentes_e = []
taxas_de_incidentes_f = []
taxas_de_incidentes_g = []
taxas_de_incidentes_h = []
taxas_de_incidentes_j = []
taxas_de_incidentes_k = []
taxas_de_incidentes_l = []

taxas_risk_acceptance_a1 = []
taxas_risk_acceptance_a2 = []
taxas_risk_acceptance_a3 = []
taxas_risk_acceptance_a = []
taxas_risk_acceptance_b = []
taxas_risk_acceptance_c = []
taxas_risk_acceptance_d = []
taxas_risk_acceptance_e = []
taxas_risk_acceptance_f = []
taxas_risk_acceptance_g = []
taxas_risk_acceptance_h = []
taxas_risk_acceptance_j = []
taxas_risk_acceptance_k = []
taxas_risk_acceptance_l = []


final_perceived_workgroup_norm_a1 = []
final_perceived_workgroup_norm_a2 = []
final_perceived_workgroup_norm_a3 = []
final_perceived_workgroup_norm_a = []
final_perceived_workgroup_norm_b = []
final_perceived_workgroup_norm_c = []
final_perceived_workgroup_norm_d = []
final_perceived_workgroup_norm_e = []
final_perceived_workgroup_norm_f = []
final_perceived_workgroup_norm_g = []
final_perceived_workgroup_norm_h = []
final_perceived_workgroup_norm_j = []
final_perceived_workgroup_norm_k = []
final_perceived_workgroup_norm_l = []

final_perceived_management_norm_a1 = []
final_perceived_management_norm_a2 = []
final_perceived_management_norm_a3 = []
final_perceived_management_norm_a = []
final_perceived_management_norm_b = []
final_perceived_management_norm_c = []
final_perceived_management_norm_e = []
final_perceived_management_norm_d = []
final_perceived_management_norm_f = []
final_perceived_management_norm_g = []
final_perceived_management_norm_h = []
final_perceived_management_norm_j = []
final_perceived_management_norm_k = []
final_perceived_management_norm_l = []

medias_comportamento_inseguro_a1 = []
medias_comportamento_inseguro_a2 = []
medias_comportamento_inseguro_a3 = []
medias_comportamento_inseguro_a = []
medias_comportamento_inseguro_b = []
medias_comportamento_inseguro_c = []
medias_comportamento_inseguro_d = []
medias_comportamento_inseguro_e = []
medias_comportamento_inseguro_f = []
medias_comportamento_inseguro_g = []
medias_comportamento_inseguro_h = []
medias_comportamento_inseguro_j = []
medias_comportamento_inseguro_k = []
medias_comportamento_inseguro_l = []


# Realização das simulações
for i in range(simulacoes):
    print(i)
    # Criação do modelo para simulação com frequência de reunião diária e treinamento bianual
    #RD-TB
    a1 = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 0.5, 0.0001, feedback, 0)
    # Adiciona a taxa de incidentes para a lista 'gerencial_diario_bianual'
    gerencial_diario_bianual.append(a1.incident_rate())
    # Adiciona as normas percebidas iniciais e finais para as listas correspondentes
    initial_perceived_workgroup_norm_a1.append(a1.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_a1.append(a1.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_a1.append(a1.worker[0].perceived_management_norm)
    final_perceived_management_norm_a1.append(a1.worker[0].perceived_management_norm)
    # Armazena a taxa de incidentes na lista
    taxa_de_incidentes_a1 = a1.incident_rate()
    taxas_de_incidentes_a1.append(taxa_de_incidentes_a1)
    # Armazena a taxa de aceitação de risco na lista
    taxa_risk_acceptance_a1 = a1.get_avg_risk_acceptance_2()
    taxas_risk_acceptance_a1.append(taxa_risk_acceptance_a1)
    # Armazena a média de comportamentos inseguros na lista
    media_comportamento_inseguro_a1 = a1.get_unsafe_behavior_media()
    medias_comportamento_inseguro_a1.append(media_comportamento_inseguro_a1)

    # Criação do modelo para simulação com frequência de reunião semanal e treinamento bianual
    #RS-TB
    a2 = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Weekly', 0.5, 0.0001, feedback, 0)
    #print('Minha vez A')
    gerencial_semanal_bianual.append(a2.incident_rate())
    initial_perceived_workgroup_norm_a2.append(a2.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_a2.append(a2.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_a2.append(a2.worker[0].perceived_management_norm)
    final_perceived_management_norm_a2.append(a2.worker[0].perceived_management_norm)
    # Armazena a taxa de incidentes na lista
    taxa_de_incidentes_a2 = a2.incident_rate()
    taxas_de_incidentes_a2.append(taxa_de_incidentes_a2)
    # Armazena a taxa de aceitação de risco na lista
    taxa_risk_acceptance_a2 = a2.get_avg_risk_acceptance_2()
    taxas_risk_acceptance_a2.append(taxa_risk_acceptance_a2)
    # Armazena a média de comportamentos inseguros na lista3
    media_comportamento_inseguro_a2 = a2.get_unsafe_behavior_media()
    medias_comportamento_inseguro_a2.append(media_comportamento_inseguro_a2)
 
    # Criação do modelo para simulação com frequência de sem diálogo e treinamento bianual
    #sR-TB
    a3 = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'None', 0.5, 0.0001, feedback, 0)
    #print('Minha vez A')
    initial_perceived_workgroup_norm_a3.append(a3.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_a3.append(a3.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_a3.append(a3.worker[0].perceived_management_norm)
    final_perceived_management_norm_a3.append(a3.worker[0].perceived_management_norm)
    gerencial_bianual.append(a3.incident_rate())
    # Armazena a taxa de incidentes na lista
    taxa_de_incidentes_a3 = a3.incident_rate()
    taxas_de_incidentes_a3.append(taxa_de_incidentes_a3)
    # Armazena a taxa de aceitação de risco na lista
    taxa_risk_acceptance_a3 = a3.get_avg_risk_acceptance_2()
    taxas_risk_acceptance_a3.append(taxa_risk_acceptance_a3)
    # Armazena a média de comportamentos inseguros na lista
    media_comportamento_inseguro_a3 = a3.get_unsafe_behavior_media()
    medias_comportamento_inseguro_a3.append(media_comportamento_inseguro_a3)

    # Criação do modelo para simulação com frequência de reunião diária e treinamento anual    
    #RD-TA
    a = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 1, 0.0001, feedback, 0)
    gerencial_diario_anual.append(a.incident_rate())
    initial_perceived_workgroup_norm_a.append(a.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_a.append(a.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_a.append(a.worker[0].perceived_management_norm)
    final_perceived_management_norm_a.append(a.worker[0].perceived_management_norm)
    taxas_de_incidentes_a.append(a.incident_rate())
    taxas_risk_acceptance_a.append(a.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_a.append(a.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião semanal e treinamento anual
    #RS-TA
    f = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Weekly', 1, 0.0001, feedback, 0)
    gerencial_semanal_anual.append(f.incident_rate())
    initial_perceived_workgroup_norm_f.append(f.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_f.append(f.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_f.append(f.worker[0].perceived_management_norm)
    final_perceived_management_norm_f.append(f.worker[0].perceived_management_norm)
    taxas_de_incidentes_f.append(f.incident_rate())
    taxas_risk_acceptance_f.append(f.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_f.append(f.get_unsafe_behavior_media())

    # Criação do modelo para simulação sem DDS e treinamento anual
    #sR-TA
    j = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 1, 0.0001, feedback, 0)
    gerencial_anual.append(j.incident_rate())
    initial_perceived_workgroup_norm_j.append(j.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_j.append(j.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_j.append(j.worker[0].perceived_management_norm)
    final_perceived_management_norm_j.append(j.worker[0].perceived_management_norm)
    taxas_de_incidentes_j.append(j.incident_rate())
    taxas_risk_acceptance_j.append(j.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_j.append(j.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião diária e treinamento semestral
    #RD-TS
    b = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 2, 0.0001, feedback, 0)
    gerencial_diario_semestral.append(b.incident_rate())
    initial_perceived_workgroup_norm_b.append(b.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_b.append(b.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_b.append(b.worker[0].perceived_management_norm)
    final_perceived_management_norm_b.append(b.worker[0].perceived_management_norm)
    taxas_de_incidentes_b.append(b.incident_rate())
    taxas_risk_acceptance_b.append(b.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_b.append(b.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião semanal e treinamento semestral
    #RS-TS
    g = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Weekly', 2, 0.0001, feedback, 0)
    gerencial_semanal_semestral.append(g.incident_rate())
    initial_perceived_workgroup_norm_g.append(g.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_g.append(g.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_g.append(g.worker[0].perceived_management_norm)
    final_perceived_management_norm_g.append(g.worker[0].perceived_management_norm)
    taxas_de_incidentes_g.append(g.incident_rate())
    taxas_risk_acceptance_g.append(g.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_g.append(g.get_unsafe_behavior_media())

    # Criação do modelo para simulação sem DDS e treinamento semestral
    #sR-TS
    k = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 2, 0.0001, feedback, 0)
    gerencial_semestral.append(k.incident_rate())
    initial_perceived_workgroup_norm_k.append(k.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_k.append(k.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_k.append(k.worker[0].perceived_management_norm)
    final_perceived_management_norm_k.append(k.worker[0].perceived_management_norm)
    taxas_de_incidentes_k.append(k.incident_rate())
    taxas_risk_acceptance_k.append(k.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_k.append(k.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião diária e treinamento trimestral
    #RD-TT
    c = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 4, 0.0001, feedback, 0)
    gerencial_diario_trimestral.append(c.incident_rate())
    initial_perceived_workgroup_norm_c.append(c.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_c.append(c.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_c.append(c.worker[0].perceived_management_norm)
    final_perceived_management_norm_c.append(c.worker[0].perceived_management_norm)
    taxas_de_incidentes_c.append(c.incident_rate())
    taxas_risk_acceptance_c.append(c.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_c.append(c.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião semanal e treinamento trimestral
    #RS-TT
    h = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Weekly', 4, 0.0001, feedback, 0)
    gerencial_semanal_trimestral.append(h.incident_rate())
    initial_perceived_workgroup_norm_h.append(h.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_h.append(h.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_h.append(h.worker[0].perceived_management_norm)
    final_perceived_management_norm_h.append(h.worker[0].perceived_management_norm)
    taxas_de_incidentes_h.append(h.incident_rate())
    taxas_risk_acceptance_h.append(h.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_h.append(h.get_unsafe_behavior_media())

    # Criação do modelo para simulação sem DDS e treinamento trimestral
    #sR-TT
    l = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 4, 0.0001, feedback, 0)
    gerencial_trimestral.append(l.incident_rate())
    initial_perceived_workgroup_norm_l.append(l.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_l.append(l.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_l.append(l.worker[0].perceived_management_norm)
    final_perceived_management_norm_l.append(l.worker[0].perceived_management_norm)
    taxas_de_incidentes_l.append(l.incident_rate())
    taxas_risk_acceptance_l.append(l.get_avg_risk_acceptance_2())
    medias_comportamento_inseguro_l.append(l.get_unsafe_behavior_media())

    # Criação do modelo para simulação com frequência de reunião diária e sem treinamento
    #RD-sT
    d = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Daily', 0.0001, 0.0001, feedback, 0)
    #print('Minha vez D')
    initial_perceived_workgroup_norm_d.append(d.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_d.append(d.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_d.append(d.worker[0].perceived_management_norm)
    final_perceived_management_norm_d.append(d.worker[0].perceived_management_norm)
    gerencial_diario.append(d.incident_rate())
    # Armazena a taxa de incidentes na lista
    taxa_de_incidentes_d = d.incident_rate()
    taxas_de_incidentes_d.append(taxa_de_incidentes_d)
    # Armazena a taxa de aceitação de risco na lista
    taxa_risk_acceptance_d = d.get_avg_risk_acceptance_2()
    taxas_risk_acceptance_d.append(taxa_risk_acceptance_d)
    # Armazena a média de comportamentos inseguros na lista
    media_comportamento_inseguro_d = d.get_unsafe_behavior_media()
    medias_comportamento_inseguro_d.append(media_comportamento_inseguro_d)

    # Criação do modelo para simulação com frequência de reunião semanal e sem treinamento
    #RS-sT
    e = Model(num_e_1, num_t_1, num_e_2, num_t_2, num_t_3, num_d, risco, 'Weekly', 0.0001, 0.0001, feedback, 0)
    #print('Minha vez E')
    initial_perceived_workgroup_norm_e.append(e.worker[0].perceived_workgroup_norm)
    final_perceived_workgroup_norm_e.append(e.worker[0].perceived_workgroup_norm)
    initial_perceived_management_norm_e.append(e.worker[0].perceived_management_norm)
    final_perceived_management_norm_e.append(e.worker[0].perceived_management_norm)
    gerencial_semanal.append(e.incident_rate())
    # Armazena a taxa de incidentes na lista
    taxa_de_incidentes_e = e.incident_rate()
    taxas_de_incidentes_e.append(taxa_de_incidentes_e)
    # Armazena a taxa de aceitação de risco na lista
    taxa_risk_acceptance_e = e.get_avg_risk_acceptance_2()
    taxas_risk_acceptance_e.append(taxa_risk_acceptance_e)
    # Armazena a média de comportamentos inseguros na lista
    media_comportamento_inseguro_e = e.get_unsafe_behavior_media()
    medias_comportamento_inseguro_e.append(media_comportamento_inseguro_e)


# Agrupamento dos resultados em listas para diferentes configurações
dds_diaria_fixa_treinamento_variavel = [gerencial_diario_bianual, gerencial_diario_anual, gerencial_diario_semestral,
                                        gerencial_diario_trimestral]

dds_semanal_fixa_treinamento_variavel = [gerencial_semanal_bianual,
    gerencial_semanal_anual, gerencial_semanal_semestral, gerencial_semanal_trimestral]
sem_dds_treiamento_variavel = [gerencial_bianual, gerencial_anual,
                               gerencial_semestral, gerencial_trimestral]

dds_variavel_sem_treinamento = [gerencial_diario, gerencial_semanal]

def export(self):
    df = pd.DataFrame({
        'history_unsafe_behavior': self.history_unsafe_behavior,
        'history_near_miss': self.history_near_miss,
        'history_near_miss_parede': self.history_near_miss_parede,
        'history_near_miss_plataforma': self.history_near_miss_plataforma,
        'history_near_miss_montadores': self.history_near_miss_montadores,
        'history_near_miss_outros': self.history_near_miss_outros,
        'history_risk_attitude': self.history_risk_attitude,
        'history_risk_acceptance': self.history_risk_acceptance,
        'history_perceived_risk': self.history_perceived_risk,
        'history_perceived_management_norm': self.history_perceived_management_norm,
        'history_perceived_workgroup_norm': self.history_perceived_workgroup_norm,
        # Adicione as novas saídas aqui
        'perceived_workgroup_norm': [worker.perceived_workgroup_norm for worker in self.worker],
        'perceived_management_norm': [worker.perceived_management_norm for worker in self.worker]
    })

    df.to_csv('gerencial_mesa_dados.csv', index=False)

media_final_incidentes = []
labels_media_final_incidentes = ['RD-TB', 'RS-TB', 'sR-TB', 'RD-TA', 'RS-TA', 'sR-TA', 'RD-TS', 'RS-TS', 'sR-TS', 'RD-TT', 'RS-TT', 'sR-TT', 'RD-sT', 'RS-sT']

# Cálculos das médias finais para as taxas de incidentes
for letra in ['a1', 'a2', 'a3', 'a', 'f','j', 'b', 'g', 'k', 'c', 'h', 'l', 'd', 'e']:
    taxa_incidentes = sum(globals()[f'taxas_de_incidentes_{letra}']) / simulacoes
    print(f"A média final da taxa de incidentes {letra} é: {taxa_incidentes}")
    media_final_incidentes.append(taxa_incidentes)

# Criação do gráfico de linhas para taxas de incidentes
plt.figure(figsize=(12, 6))
plt.plot(labels_media_final_incidentes, media_final_incidentes, marker='o', color='red', label='Taxa de Incidentes')

# Adicionando título e rótulos dos eixos
plt.title('Média Final das Taxas de Incidentes por Simulação')
plt.xlabel('Simulações')
plt.ylabel('Média Final da Taxa de Incidentes')

# Adicionando legenda e grade
plt.legend()
plt.grid(True)

# Exibindo o gráfico
plt.show()

# Configurações do gráfico de barras
cores = plt.cm.viridis(np.linspace(0, 1, len(labels_media_final_incidentes)))
plt.figure(figsize=(14, 7))
barras = plt.bar(labels_media_final_incidentes, media_final_incidentes, color=cores)

# Adicionando um padrão de textura às barras
for barra in barras:
    barra.set_hatch('°')

# Adicionando título e rótulos dos eixos
plt.title('Média Final das Taxas de Incidentes por Simulação', fontsize=16)
plt.xlabel('Simulações', fontsize=14)
plt.ylabel('Média Final da Taxa de Incidentes', fontsize=14)

# Adicionando legenda e grade
plt.legend(['Taxa de Incidentes'], fontsize=12)
plt.grid(axis='y', linestyle='--', linewidth=0.5)

# Ajustando as margens e exibindo o gráfico
plt.tight_layout()
plt.show()

media_final_comportamentos_inseguros = []
labels_media_final_comportamentos_inseguros = ['RD-TB', 'RS-TB', 'sR-TB', 'RD-TA', 'RS-TA', 'sR-TA', 'RD-TS', 'RS-TS', 'sR-TS', 'RD-TT', 'RS-TT', 'sR-TT', 'RD-sT', 'RS-sT']


# Cálculos das médias finais para comportamenros inseguros
for letra in ['a1', 'a2', 'a3', 'a', 'f','j', 'b', 'g', 'k', 'c', 'h', 'l', 'd', 'e']:
    comportamento_inseguro = sum(globals()[f'medias_comportamento_inseguro_{letra}']) / simulacoes
    print(f"A média final de comportamentos inseguros de {letra} é: {comportamento_inseguro}")
    media_final_comportamentos_inseguros.append(comportamento_inseguro)

# Criação do gráfico de linhas para comportamentos insegurosplt.figure(figsize=(10, 5))
plt.figure(figsize=(12, 6))
plt.plot(labels_media_final_comportamentos_inseguros, media_final_comportamentos_inseguros, marker='s', color='blue', label='Comportamentos Inseguros')

# Adicionando título e rótulos dos eixos
plt.title('Média Final dos Comportamentos Inseguros por Simulação')
plt.xlabel('Simulações')
plt.ylabel('Média Final de Comportamentos Inseguros')

# Adicionando legenda e grade
plt.legend()
plt.grid(True)

# Exibindo o gráfico
plt.show()

workgroup_norms = []
management_norms = []
labels_norms = ['RD-TB', 'RS-TB', 'sR-TB', 'RD-TA', 'RS-TA', 'sR-TA', 'RD-TS', 'RS-TS', 'sR-TS', 'RD-TT', 'RS-TT', 'sR-TT', 'RD-sT', 'RS-sT']

for letra in ['a1', 'a2', 'a3', 'a', 'f','j', 'b', 'g', 'k', 'c', 'h', 'l', 'd', 'e']:
    workgroup_norm = calcular_media(globals()[f'initial_perceived_workgroup_norm_{letra}'] + globals()[f'final_perceived_workgroup_norm_{letra}'])
    management_norm = calcular_media(globals()[f'initial_perceived_management_norm_{letra}'] + globals()[f'final_perceived_management_norm_{letra}'])
    workgroup_norms.append(workgroup_norm)
    management_norms.append(management_norm)

# Configurações das barras
bar_width = 0.35
index = np.arange(len(labels_norms))

# Configurando o tamanho da figura antes de criar as barras
plt.figure(figsize=(12, 6))

# Criando as barras para as normas do grupo de trabalho
plt.bar(index, workgroup_norms, bar_width, label='Norma do Grupo de Trabalho')

# Criando as barras para as normas da gestão
plt.bar(index + bar_width, management_norms, bar_width, label='Norma da Gestão')

# Adicionando rótulos e título
plt.xlabel('Parâmetros')
plt.ylabel('Valores das Normas')
plt.title('Comparação das Normas Percebidas do Grupo de Trabalho e da Gestão')
plt.xticks(index + bar_width / 2, labels_norms)
plt.legend()

# Exibindo o gráfico
plt.tight_layout()
plt.show()


# Criação dos gráficos de caixa para visualização dos resultados
fig1 = plt.figure(1)
plt.boxplot(dds_diaria_fixa_treinamento_variavel)
plt.xlabel('DDS Diária e Treinamento Variável')
plt.ylabel('Taxa de incidentes')
plt.xticks([1, 2, 3, 4], ['Bianual', 'Anual', 'Semestral', 'Trimestral'])
plt.savefig('05_dds_diaria_fixa_treinamento_variavel.png')

fig2 = plt.figure(2)
plt.boxplot(dds_semanal_fixa_treinamento_variavel)
plt.xlabel('DDS Semanal e Treinamento Variável')
plt.ylabel('Taxa de incidentes')
plt.xticks([1, 2, 3, 4], ['Bianual', 'Anual', 'Semestral', 'Trimestral'])
plt.savefig('05_dds_semanal_fixa_treinamento_variavel.png')

fig3 = plt.figure(3)
plt.boxplot(sem_dds_treiamento_variavel)
plt.xlabel('Sem DDS e Treinamento Variável')
plt.ylabel('Taxa de incidentes')
plt.xticks([1, 2, 3, 4], ['Bianual', 'Anual', 'Semestral', 'Trimestral'])
plt.savefig('05_sem_dds_treiamento_variavel.png')

fig4 = plt.figure(4)
plt.boxplot(dds_variavel_sem_treinamento)
plt.xlabel('DDS Variável e Sem Treinamento')
plt.ylabel('Taxa de incidentes')
plt.xticks([1, 2], ['Diária', 'Semanal'])
plt.savefig('05_dds_variavel_sem_treinamento.png')
plt.grid(True)
plt.show()


# Supondo que 'simulacoes' é o número total de simulações
simulacao = 14

# Cálculo das médias das percepções e aceitação de risco ao longo das simulações
workgroup_norms = []
management_norms = []
risk_acceptance = []

# Cálculos das médias finais para as taxas de risco aceitável
for letra in ['a1', 'a2', 'a3', 'a', 'f','j', 'b', 'g', 'k', 'c', 'h', 'l', 'd', 'e']:
    # Calcula a média da taxa de risco aceitável
    taxa_risk_acceptance = sum(globals()[f'taxas_risk_acceptance_{letra}']) / simulacao
    print(f"A média final da taxa risco aceitável do {letra} é: {taxa_risk_acceptance}")
    risk_acceptance.append(taxa_risk_acceptance)

    # Calcula a média das normas percebidas do grupo de trabalho
    workgroup_norm = calcular_media(globals()[f'initial_perceived_workgroup_norm_{letra}'] + globals()[f'final_perceived_workgroup_norm_{letra}'])
    workgroup_norms.append(workgroup_norm)
    
    # Calcula a média das normas percebidas da gestão
    management_norm = calcular_media(globals()[f'initial_perceived_management_norm_{letra}'] + globals()[f'final_perceived_management_norm_{letra}'])
    management_norms.append(management_norm)

# Labels para o eixo X do gráfico
labels_acceptance = ['RD-TB', 'RS-TB', 'sR-TB', 'RD-TA', 'RS-TA', 'sR-TA', 'RD-TS', 'RS-TS', 'sR-TS', 'RD-TT', 'RS-TT', 'sR-TT', 'RD-sT', 'RS-sT']

# Verifique se o número de rótulos corresponde ao número de valores nas listas de dados
assert len(labels_acceptance) == len(workgroup_norms) == len(management_norms) == len(risk_acceptance), "As listas devem ter o mesmo número de elementos."

# Criação do gráfico de linhas
plt.figure(figsize=(12, 6))

# Linhas para cada conjunto de dados
plt.plot(labels_acceptance, workgroup_norms, label='Norma de Grupo de Trabalho Percebida', marker='o')
plt.plot(labels_acceptance, management_norms, label='Norma de Gestão Percebida', marker='s')
plt.plot(labels_acceptance, risk_acceptance, label='Aceitação de Risco', marker='^')

# Adicionando título e rótulos dos eixos
plt.title('Nível de Risco Aceitável e Aceitação de Risco ao Longo das Simulações')
plt.xlabel('Simulações')
plt.ylabel('Nível de Risco')

# Adicionando legenda e grade
plt.legend()
plt.grid(True)

# Exibindo o gráfico
plt.show()
