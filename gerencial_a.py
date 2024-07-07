# Biblioteca Mesa
from pyexpat import model
import mesa
import csv

# Classes e métodos necessários da biblioteca Mesa
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import pandas as pd

# Bibliotecas diversas
import numpy as np
import seaborn
seaborn.set()

# Definindo a classe do agente Worker, que representa um trabalhador na simulação
class Worker(mesa.Agent):

    # Método utilizado para a inicialização da classe Worker
    def __init__(self, model, worker_id, crew, crew_type, p_unsafe_condition, risk_perception_coeff, attitude_change,
                 perceived_workgroup_norm, memory_capa, perceived_management_norm, min_risk_acceptance,
                 max_risk_acceptance, error_rate, weight_social, risk_attitude, freq_reun,
                 freq_trein_1):
        
        self.total_safe_behaviors = 0  # Inicializando o contador total de comportamentos seguros
        self.total_unsafe_behaviors = 0  # Inicializando o contador total de comportamentos inseguros
    
        # Variáveis de estado do agente Worker
        self.model = model  # Referência ao modelo
        self.worker_id = worker_id  # ID do trabalhador
        self.crew_type = crew_type  # Tipo de equipe (Equipe 1 - Montadores. Equipe 2 - Montadores de plataforma)
        self.crew = crew  # Equipe do trabalhador
        self.p_unsafe_condition = p_unsafe_condition  # Probabilidade de condição insegura no canteiro
        self.actual_risk = 0  # Risco real

        # Coeficiente de percepção de risco é determinado pela mudança na atitude de risco
        self.risk_perception_coeff = risk_perception_coeff
        self.attitude_change = attitude_change  # Mudança na atitude de risco

        # Norma de grupo de trabalho percebida
        self.perceived_workgroup_norm = perceived_workgroup_norm

        # Capacidade de memória do trabalhador
        self.memory_capa = memory_capa

        # Norma percebida da gestão
        self.perceived_management_norm = perceived_management_norm
        self.perceived_manager_risk_acceptance = perceived_management_norm

        # Aceitação de risco máximo e mínimo
        self.max_risk_acceptance = max_risk_acceptance
        self.min_risk_acceptance = min_risk_acceptance

        # Taxa de erro ao realizar uma atividade segura
        self.error_rate = error_rate

        # Peso social do trabalhador
        self.weight_social = weight_social

        # Atitude de risco do trabalhador
        self.risk_attitude = risk_attitude

        # Frequência de reuniões
        self.freq_reun = freq_reun

        # Frequências de treinamento transformadas em dias entre os treinamentos
        self.freq_trein_1 = 360 / freq_trein_1 

        # Contadores de dias
        self.day = 1
        self.day2 = 1
        self.day3 = 1
        self.day4 = 1

        # Ação gerencial aleatória
        self.managerial_action = np.random.uniform(0.4, 0.6)

        # Percepção de risco percebida, gerada aleatoriamente
        self.perceived_risk = 0

        # Mudança na atitude gerencial
        self.managerial_attitude_change = 0

        # Perdas diárias
        self.daily_lost = 0
        self.lost_freq_trein_1 = 0

        # Contadores de meses
        self.month_1 = 1
        self.month_2 = 1

        # Fator de influência na atitude gerencial
        self.fma = 0.5

        # Taxas de treinamento
        self.taxa_2 = 0
        self.taxa_1 = 0

        # Sorteio para determinar se o agente terá ou não um comportamento perigoso
        if np.random.uniform(0, 1) > 0.5:
            self.unsafe_behavior = 0

        else:
            self.unsafe_behavior = 1

        # Lista de vizinhos e comportamento do grupo de trabalho
        self.neighbor_list = []
        self.workgroup_behavior = []

        # Verifica se o agente está em uma condição insegura
        if np.random.uniform(0, 1) < self.p_unsafe_condition:
            self.unsafe_condition = 1
        else:
            self.unsafe_condition = 0

    def hazard_detection(self):
        if np.random.uniform(0, 1) < self.p_unsafe_condition:
            self.unsafe_condition = 1
        else:
            self.unsafe_condition = 0

    def perceiving_risk(self):
        self.risk_perception_coeff -= self.attitude_change

        self.perceived_risk = self.actual_risk * self.risk_perception_coeff

        if self.perceived_risk > 1.0:
            self.perceived_risk = 1.0
        else:
            self.perceived_risk = self.perceived_risk

        return

    def perceiving_workgroup_norm(self):
        self.previous_perceievd_workgroup_norm = self.perceived_workgroup_norm

        if len(self.workgroup_behavior) == 0:
            self.perceived_workgroup_norm = self.previous_perceievd_workgroup_norm
        else:
            self.avgerage_workgroup_behavior = sum(
                self.workgroup_behavior) / len(self.workgroup_behavior)

            self.perceived_workgroup_norm = (1 - 1 / self.memory_capa) * self.previous_perceievd_workgroup_norm + (
                1 / self.memory_capa) * self.avgerage_workgroup_behavior

        return

    def perceiving_management_norm(self):
        self.previous_perceievd_management_norm = self.perceived_management_norm

        self.perceived_management_norm = (1 - 1 / self.memory_capa) * self.previous_perceievd_management_norm + (
            1 / self.memory_capa) * self.perceived_manager_risk_acceptance

        return

    def determining_risk_acceptance(self):
        if np.random.uniform(0, 1) < self.model.r_square:
            self.risk_acceptance = (1 - self.weight_social) * self.risk_attitude + self.weight_social * (
                (self.perceived_management_norm + self.perceived_workgroup_norm) / 2)
        else:
            self.risk_acceptance = np.random.uniform(
                self.min_risk_acceptance, self.max_risk_acceptance)

        return

    def decision_making(self):
        if self.perceived_risk >= self.risk_acceptance:
            if np.random.uniform(0, 1) < self.error_rate:
                self.unsafe_behavior = 1  
                self.total_unsafe_behaviors += 1  
            else:
                self.unsafe_behavior = 0  
                self.total_safe_behaviors += 1  
        else:
            self.unsafe_behavior = 1  
            self.total_unsafe_behaviors += 1  


    def receiving_manager_feedback(self):
        if np.random.uniform(0, 1) < self.model.feedback_frequency:
            if np.random.uniform(0, 1) < 0.3:
                if self.unsafe_behavior == 1:
                    self.manager_feedback = 0  # Com feedback negativo
                else:
                    self.manager_feedback = 1  # Com feedback positivo
            else:
                self.manager_feedback = 0  # Sem feedback
        else:
            self.manager_feedback = 0  # Sem feedback

        return self.manager_feedback

    def updating_manager_standard(self):
        if self.unsafe_behavior == 0:
            if self.manager_feedback == 1:
                self.perceived_manager_risk_acceptance = np.random.uniform(
                    0, self.perceived_risk)
            else:
                self.perceived_manager_risk_acceptance = self.perceived_manager_risk_acceptance 
        else:
            
            if self.manager_feedback == 1:
                self.perceived_manager_risk_acceptance = np.random.uniform(
                    0, self.perceived_risk)
            
            else:
                self.perceived_manager_risk_acceptance = np.random.uniform(
                    self.perceived_risk, 1)

        return

    def near_miss_occurrence(self):
       
        if self.unsafe_behavior == 1 or self.unsafe_behavior == 2:
            if np.random.uniform(0, 1) < self.model.near_miss_occurence_coeff * self.actual_risk:
                self.near_miss = 1
            else:
                self.near_miss = 0
        else:
            self.near_miss = 0

        return self.near_miss

    def updating_risk_attitude(self):
        self.previous_risk_attitude = self.risk_attitude

        if self.unsafe_behavior == 1:
            if self.near_miss == 0:
                self.attitude_change = self.model.optimism_rate
            else:
                self.attitude_change = -self.model.arousal_rate
        else:
            self.attitude_change = 0

        self.risk_attitude = self.previous_risk_attitude + self.attitude_change

    def updating_risk_attitude_2(self):
        self.previous_risk_attitude = self.risk_attitude
        self.attitude_change = 0

        # ------------------- AÇÕES GERENCIAIS ---------------------
        if self.month_1 == 0:
            if self.day2 % 30 == 0:
                self.lost_freq_trein_1 = self.taxa_1
                self.month_1 = 1
        else:
            self.lost_freq_trein_1 = 0

        if self.day2 == self.freq_trein_1:
            self.attitude_change += - np.random.uniform(
                self.model.arousal_rate_min, self.model.arousal_rate_max)
            self.month_1 = 0
            self.taxa_1 = - np.random.uniform(
                self.model.arousal_rate_min, self.model.arousal_rate_max)
            self.day2 = 1

        else: #Diálogo Diário de Segurança 
            self.day2 += 1
            self.day4 += 1
            if self.freq_reun == 1:
                if self.model.near_miss_existence > 0:
                    self.attitude_change += - np.random.uniform(
                        0, self.model.optimism_rate)
                else:
                    self.attitude_change += 0
            elif self.freq_reun == 0:
                if self.day3 == 7:
                    if self.model.near_miss_existence > 0:
                        self.attitude_change += -np.random.uniform(
                            0, self.model.optimism_rate)
                    else:
                        self.attitude_change += 0
                else:
                    if self.model.near_miss_existence > 0:
                        self.attitude_change += -self.model.optimism_rate
                    else:
                        self.attitude_change += self.model.optimism_rate
                    self.day3 += 1
            else:
                self.attitude_change += 0


        return
    
# In[11]:

class Model(mesa.Model):

    def __init__(self, num_crews_1, num_worker_per_crew_1, num_crews_2, num_worker_per_crew_2, num_other_workers,
                 n_steps, activity_risk, freq_reun, freq_trein_1, feedback_frequency):
        """
        Método de inicialização da classe Model.
        """
        
        # Atributos da instância do modelo
        self.nsteps = n_steps  # Número total de etapas de simulação
        self.running = True 
        
        # Número de equipes e trabalhadores por equipe
        self.num_crews_1 = num_crews_1
        self.num_worker_per_crew_1 = num_worker_per_crew_1
        self.num_crews_2 = num_crews_2
        self.num_worker_per_crew_2 = num_worker_per_crew_2
        self.num_other_workers = num_other_workers
        self.total_workers = num_crews_1 * num_worker_per_crew_1 + \
                             num_crews_2 * num_worker_per_crew_2 + num_other_workers
        
        # Parâmetros do modelo
        self.activity_risk = activity_risk  # Risco da atividade
        self.num_steps = n_steps
        self.ingroup_obs_ratio = 1
        self.outgroup_obs_ratio = 0.03
        self.error_rate = 0.01  # Taxa de erro
        self.min_risk_perception_coeff = 0.6  # Coeficiente mínimo de percepção de risco
        self.max_risk_perception_coeff = 1.2  # Coeficiente máximo de percepção de risco
        self.min_perceived_workgroup_norm = 0.1  # Norma mínima percebida do grupo de trabalho
        self.max_perceived_workgroup_norm = 0.9  # Norma máxima percebida do grupo de trabalho
        self.min_perceived_management_norm = 0.1  # Norma mínima percebida da gestão
        self.max_perceived_management_norm = 0.9  # Norma máxima percebida da gestão
        self.memory_capa = 15  # Capacidade de memória
        self.min_manager_standard = 0.2  # Padrão mínimo do gerente
        self.max_manager_standard = 0.3  # Padrão máximo do gerente
        self.attitude_change = 0  # Mudança de atitude
        self.weight_social = 0.75  # Peso social
        self.near_miss_occurence_coeff = 0.01 # Coeficiente de ocorrência de quase acidente
        self.min_risk_acceptance = 0.1  # Aceitação mínima de risco
        self.max_risk_acceptance = 0.9  # Aceitação máxima de risco
        self.min_risk_attitude = 0.1  # Atitude mínima em relação ao risco
        self.max_risk_attitude = 0.9  # Atitude máxima em relação ao risco
        self.min_project_identity = 0.1  # Identidade mínima do projeto
        self.max_project_identity = 0.9  # Identidade máxima do projeto
        self.r_square = 0.85  # Coeficiente de determinação
        self.feedback_frequency = feedback_frequency  # Frequência de feedback
        self.arousal_rate = 0.2  # Taxa de excitação
        self.arousal_rate_min = 0.2  # Taxa mínima de excitação (teste do feedback)
        self.arousal_rate_max = 0.3  # Taxa máxima de excitação (teste do feedback)
        self.optimism_rate = 0.001  # Taxa de otimismo
        self.near_miss_existence = 0

        if freq_reun == 'Diário':
            self.freq_reun = 1
        elif freq_reun == 'Semanal':
            self.freq_reun = 0
        elif freq_reun == 'None':
            self.freq_reun = 2
        else:
            self.running = False
            print('Erro: Frequência de reunião inválida')

        self.freq_trein_1 = freq_trein_1  # Frequência de treinamento        
        self.t = 1  # Tempo inicial
        self.worker = []  # Lista de trabalhadores

        # Saídas a cada step
        self.history_unsafe_behavior = []
        self.history_near_miss = []
        self.history_near_miss_parede = []
        self.history_near_miss_outros = []
        self.history_near_miss_plataforma = []
        self.history_near_miss_montadores = []
        self.history_risk_attitude = []
        self.history_perceived_risk = []
        self.history_risk_acceptance = []
        self.history_perceived_workgroup_norm = []
        self.history_perceived_management_norm = []
        self.history_incident_rate = []
        self.history_unsafe_behavior_ratio = []
        
        # Configuração das variáveis de histórico
        self.setup_worker()  # Configuração dos trabalhadores
        self.datacollector_risk = DataCollector({
            "Risk Attitude Average": Model.get_avg_risk_attitude,
            "Average Risk Tolerance": Model.get_avg_risk_acceptance,
            "Average Risk Perception": Model.get_avg_risk_perception
        })  # Coletor de dados para risco
        self.datacollector_behavior = DataCollector({
            "Unsafe Behaviors": Model.get_unsafe_behavior,
            "Near Misses": Model.get_near_miss
        })  # Coletor de dados para comportamento
        

    # Método para configurar os trabalhadores no modelo
    def setup_worker(self):
        
        range_1 = self.num_crews_1 * self.num_worker_per_crew_1
        a = 1
        id = 0
        for i in range(range_1):
            if i % self.num_worker_per_crew_1 == 0:
                a += 1
            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=1,
                                    p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                        self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein_1=self.freq_trein_1))
            id += 1

        for j in range(self.num_crews_2 * self.num_worker_per_crew_2):
            if j % self.num_worker_per_crew_1 == 0:
                a += 1
            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=2,
                                    p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                        self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein_1=self.freq_trein_1, )) 
            id += 1

        a += 1
        for k in range(self.num_other_workers):
            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=3,
                                    p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                        self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein_1=self.freq_trein_1,))
            id += 1

    # Método para determinar os vizinhos de cada trabalhador
    def get_worker_neighbors(self):
        """
        Método para determinar os vizinhos de cada trabalhador
        """
        for i in range(self.total_workers):
            del self.worker[i].neighbor_list[0:len(
                self.worker[i].neighbor_list)]
            for j in range(self.total_workers):
                if j == self.worker[i].worker_id:
                    self.worker[i].neighbor_list = self.worker[i].neighbor_list
                else:
                    if self.worker[j].crew == self.worker[i].crew:
                        if np.random.uniform(0, 1) < self.ingroup_obs_ratio:
                            self.worker[i].neighbor_list.append(j)
                        else:
                            self.worker[i].neighbor_list == self.worker[i].neighbor_list
                    else:
                        if np.random.uniform(0, 1) < self.outgroup_obs_ratio:
                            self.worker[i].neighbor_list.append(j)
                        else:
                            self.worker[i].neighbor_list = self.worker[i].neighbor_list

    def get_near_miss_x(self):
        """
        Método para calcular o número total de quase acidentes em uma equipe
        """
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.near_miss
        #print(total)
        return total

    # Método para interagir entre trabalhadores
    def step_interact(self):
        
        self.get_worker_neighbors()
        self.near_miss_existence_vector = []
        random_order = list(
            range(self.total_workers))
        np.random.shuffle(random_order)

        for i in random_order:

            if self.worker[i].crew_type == 2:
                self.worker[i].actual_risk = random.betavariate( 10 * self.activity_risk
                    ,4.5-5*self.activity_risk)
            else:
                self.worker[i].actual_risk = random.betavariate(
                    5 * self.activity_risk, 5-5*self.activity_risk)

            self.worker[i].hazard_detection()

            if self.worker[i].unsafe_condition == 0:
                if np.random.uniform(0, 1) < self.error_rate:
                    self.worker[i].unsafe_behavior = 2
                    self.worker[i].near_miss_occurrence()
                    if self.worker[i].near_miss == 1:
                        self.worker[i].attitude_change = - \
                            self.arousal_rate
                    else:
                        self.worker[i].attitude_change = 0
                    self.worker[i].risk_attitude += self.worker[i].attitude_change
                else:
                    self.worker[i].unsafe_behavior = 0
                    self.worker[i].near_miss_occurrence()
                    self.worker[i].attitude_change = 0
                    self.worker[i].risk_attitude += self.worker[i].attitude_change
            else:
                self.worker[i].perceiving_risk()

                del self.worker[i].workgroup_behavior[0:len(
                    self.worker[i].workgroup_behavior)]

                for j in self.worker[i].neighbor_list:

                    if self.worker[j].unsafe_condition == 1:
                        if self.worker[j].unsafe_behavior == 0:
                            observation = np.random.uniform(
                                0, self.worker[j].actual_risk)
                        elif self.worker[j].unsafe_behavior == 1:
                            observation = np.random.uniform(
                                self.worker[j].actual_risk, 1)
                            self.worker[i].workgroup_behavior.append(
                                observation)
                        else:
                            print(self.worker[j].unsafe_behavior, "= error")
                    else:
                        self.worker[i].workgroup_behavior = self.worker[i].workgroup_behavior

                self.worker[i].perceiving_workgroup_norm()
                self.worker[i].perceiving_management_norm()
                self.worker[i].determining_risk_acceptance()
                self.worker[i].decision_making()
                self.worker[i].receiving_manager_feedback()
                self.worker[i].updating_manager_standard()
                self.worker[i].near_miss_occurrence()
                self.worker[i].updating_risk_attitude()
            self.worker[i].updating_risk_attitude_2()
            self.worker[i].determining_risk_acceptance()
            self.worker[i].perceiving_risk()

        self.near_miss_existence = self.get_near_miss_x()


    # Função para calcular a percepção média de risco entre todos os trabalhadores
    @staticmethod
    def get_avg_risk_perception(self):
        total = 0
        a = 0
        for worker in self.worker: 
            if worker.crew_type != 3:
                total += worker.perceived_risk
                a = a + 1
        return total / a

    # Função para calcular o número total de comportamentos inseguros
    @staticmethod
    def get_unsafe_behavior(self):
        total_safe_behavior = 0
        total_unsafe_behavior = 0 
        for worker in self.worker:
            if worker.unsafe_behavior == 0:
                total_safe_behavior += 1
            else:
                total_unsafe_behavior += 1

        total_comportamentos = total_safe_behavior + total_unsafe_behavior
        media_comportamentos_inseguros = total_unsafe_behavior / total_comportamentos
       
        #print(media_comportamentos_inseguros)

        return total_safe_behavior, total_unsafe_behavior, media_comportamentos_inseguros
    
    # Função para calcular o número total de quase acidentes
    @staticmethod
    def get_near_miss(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.near_miss
        return total

    # Função para calcular a atitude média em relação ao risco entre todos os trabalhadores
    @staticmethod
    def get_avg_risk_attitude(self):
        total = 0
        a = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_attitude
                a = a + 1
        return total / a

    # Método de instância para calcular a aceitação média de risco entre todos os trabalhadores
    def get_avg_risk_acceptance(self):
        total = 0
        a = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_acceptance
                a += 1
        return total / a if a > 0 else 0  # Verificação para evitar divisão por zero

    def get_avg_risk_perception_2(self):
        total = 0
        a=0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.perceived_risk
                a=a+1
        return total / a

    def get_unsafe_behavior_2(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                if worker.unsafe_behavior == 1 or worker.unsafe_behavior == 2:
                    total += 1
                else:
                    total = total
        return total

    def get_near_miss_2_parede(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type == 1:
                total += worker.near_miss
        return total

    def get_near_miss_2_plataforma(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type == 2:
                total += worker.near_miss
        return total

    def get_near_miss_2_outros(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type == 3:
                total += worker.near_miss
        return total

    def get_near_miss_2_todos(self):
        total = 0
        for worker in self.worker:
            total += worker.near_miss
        return total

    def get_avg_risk_attitude_2(self):
        total = 0
        a=0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_attitude
                a=a+1
        return total / a

    def get_avg_risk_acceptance_2(self):
        total = 0
        a=0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_acceptance
                a = a+1
        taxa_risk_acceptance = total / a
        return taxa_risk_acceptance
    
    def get_perceived_management_norm(self):
        total = 0
        for worker in self.worker:
                total += worker.perceived_management_norm
        return total / len(self.worker)
    def get_perceived_workgroup_norm (self):
        total = 0
        for worker in self.worker:
                total += worker.perceived_workgroup_norm
        return total / len(self.worker)

    def info_matrix(self):
        matrix = np.array([self.history_near_miss, self.history_near_miss_parede, self.history_near_miss_plataforma,
                           self.history_near_miss_montadores, self.history_near_miss_outros, self.history_risk_attitude,
                           self.history_risk_acceptance, self.history_perceived_risk])
        return matrix

    def incident_rate(self):
        total_near_miss = sum(self.history_near_miss)
        total_working_hour = (self.nsteps)*(self.total_workers)*8
        taxa_de_incidentes = (total_near_miss/total_working_hour)*(200000/10) 
        return taxa_de_incidentes
    
    def incident_rate_1(self):
        total_near_miss = sum(self.history_near_miss_parede)
        total_working_hour = (
            self.nsteps)*(self.num_crews_1*self.num_worker_per_crew_1)*8
        return (total_near_miss/total_working_hour)*(200000/10)


    def incident_rate_2(self):
        total_near_miss = sum(self.history_near_miss_plataforma)
        total_working_hour = (
            self.nsteps)*(self.num_crews_2*self.num_worker_per_crew_2)*8
        return (total_near_miss/total_working_hour)*(200000/10)


    def incident_rate_3(self):
        total_near_miss = sum(self.history_near_miss_montadores)
        total_working_hour = (
            self.nsteps)*(self.num_crews_1*self.num_worker_per_crew_1+self.num_crews_2*self.num_worker_per_crew_2)*8
        return (total_near_miss/total_working_hour)*(200000/10)


    def incident_rate_4(self):
        total_near_miss = sum(self.history_near_miss_outros)
        total_working_hour = (
            self.nsteps)*(self.num_other_workers)*8
        return (total_near_miss/total_working_hour)*(200000/10)

    
    def get_unsafe_behavior_2(self):
        total = 0
        for worker in self.worker:
            if worker.unsafe_behavior == 1 or worker.unsafe_behavior == 2:
                total += 1
            else:
                total = total
        return total
    
    def get_unsafe_behavior_media(self):
        # Calcula a média de comportamentos inseguros
        unsafe_behavior_media = sum(self.history_unsafe_behavior) / len(self.history_unsafe_behavior)
        return unsafe_behavior_media
       

    
    

    def export(self):
        # Cria o DataFrame com os arrays
        df = pd.DataFrame({'history_unsafe_behavior': self.history_unsafe_behavior,
                            'history_near_miss': self.history_near_miss,
                           'history_near_miss_parede': self.history_near_miss_parede,
                           'history_near_miss_plataforma': self.history_near_miss_plataforma,
                           'history_near_miss_montadores': self.history_near_miss_montadores,
                           'history_near_miss_outros': self.history_near_miss_outros,
                           'history_risk_attitude': self.history_risk_attitude,
                           'history_risk_acceptance': self.history_risk_acceptance,
                           'history_perceived_risk': self.history_perceived_risk,
                           'history_perceived_management_norm':self.history_perceived_management_norm,
                           'history_perceived_workgroup_norm': self.history_perceived_workgroup_norm})

        # exportando o DataFrame para um arquivo CSV
        df.to_csv('gerencial_mesa_dados.csv', index=False)

    def step(self):

        self.step_interact()
        #  MESA COLLECTORS
        self.datacollector_risk.collect(self)
        self.datacollector_behavior.collect(self)

        # Arrays para outros gráficos
        self.history_unsafe_behavior.append(self.get_unsafe_behavior_2())
        self.history_near_miss.append(self.get_near_miss_2_todos())

        self.history_near_miss_parede.append(self.get_near_miss_2_parede())
        self.history_near_miss_outros.append(self.get_near_miss_2_outros())
        self.history_near_miss_plataforma.append(
            self.get_near_miss_2_plataforma())
        self.history_near_miss_montadores.append(
            (self.get_near_miss_2_plataforma() + self.get_near_miss_2_parede())/2)

        self.history_risk_attitude.append(self.get_avg_risk_attitude_2())
        self.history_risk_acceptance.append(self.get_avg_risk_acceptance_2())
        self.history_perceived_risk.append(self.get_avg_risk_perception_2())
        self.history_perceived_management_norm.append(self.get_perceived_management_norm())
        self.history_perceived_workgroup_norm.append(self.get_perceived_workgroup_norm ())

        self.t = self.t+1

        if self.t - 2 == self.nsteps:
            self.export()
            self.running = False
        return
