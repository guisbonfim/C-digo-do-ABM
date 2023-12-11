# coding: utf-8

# In[9]:
import mesa
# from statistics import mean

from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import pandas as pd
# import networkx as nx
# from mesa.space import NetworkGrid, MultiGrid
# get_ipython().magic('matplotlib inline')
# Standard imports
# import copy
# import itertools

# Scientific computing imports
import numpy as np
# import networkx
# import pandas as pd
import seaborn
seaborn.set()

# Import widget methods

# In[10]:


class Worker (mesa.Agent):

    """
    Worker class encapsulate the socio-cognitive process of worker's safety behavior
    """

    def __init__(self, model, worker_id, crew, crew_type, p_unsafe_condition, risk_perception_coeff, attitude_change,
                 perceived_workgroup_norm, memory_capa, perceived_management_norm, min_risk_acceptance,
                 max_risk_acceptance, error_rate, weight_social, risk_attitude, freq_reun,
                 freq_trein):  # manageri

        # self permite que a variavel seja compartilhada entre todas as funçoes de uma classe

        # OS COMETARIOS AOS LADOS SÃO COMO SERAO DEFINIDAS AS VARIAVEIS DESSA CLASSE QUANDO FOREM CHAMADAS PELA OUTRA CLASSE(QUE TEM SUAS PRÓPRIAS VARIAVEIS, SENDO ALGUMAS IGUAIS)
        self.model = model  # model=self
        self.worker_id = worker_id  # worker_id=j+i*self.num_worker_per_crew
        self.crew_type = crew_type  # crew_type=i
        self.crew = crew
        # na outra classe vi que esse é o risco do canteiro -> p_unsafe_condition=self
        self.p_unsafe_condition = p_unsafe_condition
        self.actual_risk = 0

        # risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff)
        self.risk_perception_coeff = risk_perception_coeff
        self.attitude_change = attitude_change  # attitude_change=self.attitude_change
        # perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm)
        self.perceived_workgroup_norm = perceived_workgroup_norm
        # acredito o que é a  capacidade de retera informação
        self.memory_capa = memory_capa  # memory_capa=self.memory_capa
        # perceived_management_norm=np.random.uniform(self.min_perceived_management_norm, self.max_perceived_management_norm)
        self.perceived_management_norm = perceived_management_norm
        self.perceived_manager_risk_acceptance = perceived_management_norm
        # max_risk_acceptance=self.max_risk_acceptance
        self.max_risk_acceptance = max_risk_acceptance
        # min_risk_acceptance=self.min_risk_acceptance
        self.min_risk_acceptance = min_risk_acceptance
        self.weight_social = weight_social  # weight_social=self.weight_social
        # risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude)
        self.risk_attitude = risk_attitude
        # project_identity=np.random.uniform(self.min_project_identity, self.max_project_identity),

        # erro ao realizar uma atividade segura -> error_rate=self.error_rate
        self.error_rate = error_rate

        # np.random.uniform() diz q todos os valores no itervalo tem q ter a mesma probalididade de ser selecionado
        # é da biblioteca NumPy e inclui o menor valor mas não o maior valor (]
        self.risk_acceptance = np.random.uniform(
            min_risk_acceptance, max_risk_acceptance)
        self.near_miss = 0

        self.freq_reun = freq_reun
        self.freq_trein = 360/freq_trein  # transformei para dias entre os treinamentos
        self.day = 1
        self.day2 = 1
        self.day3 = 1
        self.managerial_action = np.random.uniform(0.4, 0.6)
        self.perceived_risk = 0
        self.managerial_attitude_change = 0
        self.daily_lost = 0
        self.lost_freq_trein = 0

        self.fma = 0.5
        # sorteio pra ver se o agente tera ou não uma ação perigosa, 0 ou 1 tem probabilidades iguais
        if np.random.uniform(0, 1) > 0.5:
            self.unsafe_behavior = 0
        else:
            self.unsafe_behavior = 1

        self.neighbor_list = []
        self.workgroup_behavior = []

        # quanto maior o p_unsafe_condition maior  a probalididade de unsafe_cndition ser 1
        if np.random.uniform(0, 1) < self.p_unsafe_condition:
            self.unsafe_condition = 1
        else:
            self.unsafe_condition = 0

    # se quisermos  ter uma novo unsafe_condition

    def hazard_detection(self):
        if np.random.uniform(0, 1) < self.p_unsafe_condition:
            self.unsafe_condition = 1
        else:
            self.unsafe_condition = 0
    # define perceived_risk a partir do  attitude change

    def perceiving_risk(self):
        # Risk perception coefficient is determined by changes in risk attitude
        # percepçao de risco vai diminuir com o aumento da attitude change
        self.risk_perception_coeff -= (self.attitude_change +
                                       self.managerial_attitude_change)/2

        # Perceived risk is a function of actual risk and risk perception coefficient
        # leva em consideração o risco real e se maior a percepção de risco mais chances dele perver o risco
        self.perceived_risk = self.actual_risk * self.risk_perception_coeff

        # Perceived risk cannot be greater than 1.0
        if self.perceived_risk > 1.0:
            self.perceived_risk = 1.0
        else:
            self.perceived_risk = self.perceived_risk

        return

    def perceiving_workgroup_norm(self):

        self.previous_perceievd_workgroup_norm = self.perceived_workgroup_norm

        # If there were not coworkers near the worker, there will be no changes in the perceived workgroup norm
        # a função len() nos diz o número de itens no vetor, neste caso se for zero não há mudanças, não há ninguem perto
        if len(self.workgroup_behavior) == 0:
            self.perceived_workgroup_norm = self.previous_perceievd_workgroup_norm
            # If not, workgroup norm is the weighted sum of previous workgroup norm and the perception of the average of workgroup behaviors
        else:
            # Calculating the average of workgroup behaviors .bs sum() SOMA OS ITENS DOS VETORES, ENTão ele esta tirando
            # a media do comportamento grupal, acredito que na outra classe cada item sera o unsafe behavior decada um
            self.avgerage_workgroup_behavior = sum(
                self.workgroup_behavior)/len(self.workgroup_behavior)
            self.perceived_workgroup_norm = (1-1/self.memory_capa)*self.previous_perceievd_workgroup_norm + (
                1/self.memory_capa) * self.avgerage_workgroup_behavior
        # a norma percebida leva em considera~]ao a norma pecebida anterior, o atual comportamento do grupo e a capacidade de memoria
        # essa última define o quanto as outras duas terao pe'so, preciso analisar os valores possiveis que a variavel  memory capa pode ter

        return

    def perceiving_management_norm(self):
        # Management norm is the weighted sum of previous management norm and the current perception of managers' risk acceptance
        self.previous_perceievd_management_norm = self.perceived_management_norm
        self.perceived_management_norm = (1-1/self.memory_capa)*self.previous_perceievd_management_norm + (
            1/self.memory_capa) * self.perceived_manager_risk_acceptance
        # pesa a norma gerencial com a atual aceitação de nivel de risco gerencial ( tudo isso em relação ao que os agentes percebem que são esses valores)
        return

    def determining_risk_acceptance(self):
        # Risk acceptance is determined by risk attitude, workgroup norm, management norm, and project identity
        # esse .model parece ser algo só para normalizar a variavel
        # elmrar que r2 ve se duas amostras são estatisticamente palusiveis etaõ se for segue
        if np.random.uniform(0, 1) < self.model.r_square:
            self.risk_acceptance = (1-self.weight_social)*self.risk_attitude + self.weight_social * (
                (self.perceived_management_norm + self.perceived_workgroup_norm)/2)
        # aqui o peso é dado pelo wight social e o project identity, alterando atitude de risco, a norma gerencial e a norma percebid a do grupo
        else:
            # If the randomly selected number is greater than r^2 in the regression analysis, risk acceptance will be randomly determined
            self.risk_acceptance = np.random.uniform(
                self.min_risk_acceptance, self.max_risk_acceptance)
        return

    def decision_making(self):
        # if perceived risk is greater than risk acceptance, the worker will perform a safe behavior
        if self.perceived_risk >= self.risk_acceptance:
            # There would be some near in executing safe behaviors
            if np.random.uniform(0, 1) < self.error_rate:
                self.unsafe_behavior = 1  # ATVD INSEGURA
            else:
                self.unsafe_behavior = 0  # ATVD SEGURA
        else:
            self.unsafe_behavior = 1  # ATVD INSEGURA
        # basicamente se a percepção de risco for maior que a aceitação do risco ele tendera a realizar uma ação segura
        # caso a porcetagem de erro em sção segura for mto alta provavelmente ele ainda realizara uma atividade insegura
        return

    def receiving_manager_feedback(self):
        # If the worker performs a safe behavior, there will be no feedback from manager
        if self.unsafe_behavior == 0:
            self.manager_feedback = 0  # SEM FEEDBACK
        else:
            # There might be some chances the worker will not receive feedback even if the worker performs an unsafe behavior
            if np.random.uniform(0, 1) < self.model.feedback_frequency:
                if self.actual_risk > np.random.uniform(self.model.min_manager_standard, self.model.max_manager_standard):
                    self.manager_feedback = 1  # COM FEEDBACK
                else:
                    self.manager_feedback = 0  # SEM FEEDBACK
            else:
                self.manager_feedback = 0  # SEM FEEDBACK

        return
    # RETORNA O PERCEIVED MANAGER RISK ACCEPTANCE

    def updating_manager_standard(self):
        # If the worker performs a safe behavior, there will be no changes in perceived managers' risk acceptance
        if self.unsafe_behavior == 0:
            self.perceived_manager_risk_acceptance = self.perceived_manager_risk_acceptance
        else:
            # If the worker receives feedback from managers, perceived managers' risk acceptance will become lower than the current perceived risk
            if self.manager_feedback == 1:
                self.perceived_manager_risk_acceptance = np.random.uniform(
                    0, self.perceived_risk)

            # If the worker does not receive feedback from managers, perceived managers' risk acceptance will become higher than the current perceived risk
            else:
                self.perceived_manager_risk_acceptance = np.random.uniform(
                    self.perceived_risk, 1)

    # NEAR MISS É  CONTRARIO DO ERROR RATE, ENTÃO O AGENTE PODE SE SAFAR DE UMA AÇÃO RUIM
    def near_miss_occurrence(self):
        # If the worker performs an unsafe behavior, there is some possibilities of the near miss
        if self.unsafe_behavior == 1 or self.unsafe_behavior == 2:

            if np.random.uniform(0, 1) < self.model.near_miss_occurence_coeff*self.actual_risk:
                self.near_miss = 1
            else:
                self.near_miss = 0
        # If the worker performs a safe behavior, there will be no near miss
        else:
            self.near_miss = 0
    # A ATITUDE EM RELAÇÃO a risco leva em cosideraçao o near miss,

    def updating_risk_attitude(self):

        self.previous_risk_attitude = self.risk_attitude
        # If there is no near miss, the worker's risk attitude will be decreased.
        if self.unsafe_behavior == 1:
            if self.near_miss == 0:
                self.attitude_change = self.model.optimism_rate  # 0.001
            # If not, the worker's risk attitude will be increased.
            else:
                self.attitude_change = -self.model.arousal_rate  # 0.2
        else:
            self.attitude_change = 0

        self.risk_attitude = self.previous_risk_attitude + self.attitude_change

    def updating_risk_attitude_2(self):

        self.previous_risk_attitude = self.risk_attitude
        # ------------------- AÇÕES GERENCIAIS ---------------------
        # definindo perda diaria
        self.daily_lost = np.random.uniform(0, 0.001)
        if self.day2 % 15 == 0:
            self.lost_freq_trein = np.random.uniform(0, 0.02)
        else:
            self.lost_freq_trein = 0

        if self.day2 == self.freq_trein:  # dia de treinamento
            self.managerial_attitude_change = - np.random.uniform(
                0.15, 0.25)
            self.day2 = 1
        else:  # avaliamos dds
            self.day2 += 1
            if self.freq_reun == 1:  # diario
                self.managerial_attitude_change = - np.random.uniform(
                    0.001, 0.002)
            elif self.freq_reun == 0:
                if self.day3 == 6:  # se tiver completado uma semana, lembrando que nos fnais de semana essa função n é chamada
                    self.managerial_attitude_change = -np.random.uniform(
                        0.001, 0.002)
                    self.day3 = 1
                else:
                    self.managerial_attitude_change = 0
                    self.day3 += 1
            else:
                self.managerial_attitude_change = 0
        self.risk_attitude = self.previous_risk_attitude + \
            self.managerial_attitude_change + self.daily_lost + \
            self.lost_freq_trein


# In[11]:


class Model (mesa.Model):
    """
    Model class, which encapsulates the entire behavior of single run of simulation model
     n_trabs, n_eqs,
    """

    def __init__(self, num_crews_1, num_worker_per_crew_1, num_crews_2, num_worker_per_crew_2, num_other_workers,
                 n_steps, activity_risk, freq_reun, freq_trein,  feedback_frequency, using_mesa):
        # , using_mesa
        # using_mesa = 1
        # Ao lado coloquei os valores das variaveis na inicialização que tem acima

        self.nsteps = n_steps
        self.running = True

        self.num_crews_1 = num_crews_1
        self.num_worker_per_crew_1 = num_worker_per_crew_1
        self.num_crews_2 = num_crews_2
        self.num_worker_per_crew_2 = num_worker_per_crew_2
        self.num_other_workers = num_other_workers
        self.total_workers = num_crews_1*num_worker_per_crew_1 + \
            num_crews_2*num_worker_per_crew_2 + num_other_workers

        self.num_steps = n_steps
        self.ingroup_obs_ratio = 1
        self.outgroup_obs_ratio = 0.03
        self.activity_risk = activity_risk  # 0.5
        self.error_rate = 0.01
        self.min_risk_perception_coeff = 1.2
        self.max_risk_perception_coeff = 0.6
        self.min_perceived_workgroup_norm = 0.1
        self.max_perceived_workgroup_norm = 0.9
        self.min_perceived_management_norm = 0.1
        self.max_perceived_management_norm = 0.9
        self.memory_capa = 15
        self.min_manager_standard = 0.2
        self.max_manager_standard = 0.4
        self.attitude_change = 0
        self.weight_social = 0.75
        self.near_miss_occurence_coeff = 0.01

        self.min_risk_acceptance = 0.1
        self.max_risk_acceptance = 0.9
        self.min_risk_attitude = 0.1
        self.max_risk_attitude = 0.9

        self.min_project_identity = 0.1
        self.max_project_identity = 0.9

        self.r_square = 0.85
        self.feedback_frequency = feedback_frequency
        self.arousal_rate = 0.2
        self.optimism_rate = 0.01

        # colocando os valores de reunioes como numeros em vez de palavras, para facilitAR
        if freq_reun == 'Daily':
            self.freq_reun = 1
        elif freq_reun == 'Weekly':
            self.freq_reun = 0
        elif freq_reun == 'None':
            self.freq_reun = 2
        else:
            self.running = False
            print('error')

        self.freq_trein = freq_trein

        self.t = 1
        self.worker = []

        # Set the history variables
        # essas serão nossas saidas a cada step
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

        # ja definindo todos os valores das variaveis e constantes de cada agente
        self.setup_worker()

        self.datacollector_risk = DataCollector({
            "Risk Attitude Average": Model.get_avg_risk_attitude,
            "Average Risk Tolerance": Model.get_avg_risk_acceptance,
            "Average Risk Perception": Model.get_avg_risk_perception, }
        )

        self.datacollector_behavior = DataCollector({
            "Unsafe Behaviors": Model.get_unsafe_behavior,
            "Near Misses": Model.get_near_miss,
        })

        # self.datacollector_risk.collect(self)
        # self.datacollector_perceived_norms.collect(self)
        # self.datacollector_behavior.collect(self)

        # SE ESTIVERMOS USANDO A FUNÇÃO COMO GERADOR DE GRÁFICOS TEMOS QUE CHAMAR O STEP VARIAS VEZES
        # SE ESTIVERMOS USANDO O MESA ELE AUTOMATICAMENTE CHAMA O MESA DIVERSAS VEZES
        if using_mesa == 0:
            for i in range(self.nsteps):
                self.step()
        else:
            self.step()

    def setup_worker(self):
        """
        Method to set up workers in the model
        """

        a = 1
        id = 0
        for i in range(self.num_crews_1*self.num_worker_per_crew_1):
            if i % self.num_worker_per_crew_1 == 0:
                a += 1

            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=1,
                                      p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                          self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein=self.freq_trein))
            id += 1

        for j in range(self.num_crews_2*self.num_worker_per_crew_2):
            # .append() adiciona itens ao vetor self.worker, ele então chama a classe worker e insere os valores
            if j % self.num_worker_per_crew_1 == 0:
                a += 1
            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=2,
                                      p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                          self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein=self.freq_trein))
            id += 1

        a += 1
        for k in range(self.num_other_workers):
            self.worker.append(Worker(model=self, worker_id=id, crew=a, crew_type=3,
                                      p_unsafe_condition=self.activity_risk, risk_perception_coeff=np.random.uniform(self.min_risk_perception_coeff, self.max_risk_perception_coeff), perceived_workgroup_norm=np.random.uniform(self.min_perceived_workgroup_norm, self.max_perceived_workgroup_norm), memory_capa=self.memory_capa, perceived_management_norm=np.random.uniform(
                                          self.min_perceived_management_norm, self.max_perceived_management_norm), min_risk_acceptance=self.min_risk_acceptance, max_risk_acceptance=self.max_risk_acceptance, error_rate=self.error_rate, attitude_change=self.attitude_change, weight_social=self.weight_social, risk_attitude=np.random.uniform(self.min_risk_attitude, self.max_risk_attitude),  freq_reun=self.freq_reun, freq_trein=self.freq_trein))
            id += 1

    # retorna quais são os vizinhos de cada agente

    def get_worker_neighbors(self):
        # range(a) cria um vetor que starta em 0 até o valor limite "a" com icremento unitário. neste caso a é a quantidade de trabalhadores
        # este primeiro for define cada um dos agentes e vamos sortear seus vizinhos
        for i in range(self.total_workers):
            # Before creating the neighbor list, deleting the previous list
            # del variavel[a:b] deleta os itens de a a b do vetor
            del self.worker[i].neighbor_list[0:len(
                self.worker[i].neighbor_list)]
            # este for é para analisar cada vizinho
            for j in range(self.total_workers):
                # Himself or herself cannot be a neighbor
                if j == self.worker[i].worker_id:
                    self.worker[i].neighbor_list = self.worker[i].neighbor_list

                else:
                    # If the j is the same workgroup member
                    if self.worker[j].crew == self.worker[i].crew:
                        # essas variaves ratio são definidas inicialmente, procar entender o porq, mas acredito que tenha que ser um numero alto entre 0 e 1 pois são da mesma equipe e tem probbilidade de estarem relmente juntos
                        if np.random.uniform(0, 1) < self.ingroup_obs_ratio:
                            self.worker[i].neighbor_list.append(j)
                            # ese append(j) esta adicionando o j como vizinho se o sorteio do random for verdadeiro
                        else:
                            # não a adicionamento de vizinho
                            self.worker[i].neighbor_list == self.worker[i].neighbor_list

                    # If the j is not the same workgroup member
                    else:
                        # ja este ratio tem q ser um numero baixo pois nã sao do mesmo grupo, mas não zero pois ainda há chances deles serem vizinhos
                        if np.random.uniform(0, 1) < self.outgroup_obs_ratio:
                            self.worker[i].neighbor_list.append(j)
                        else:
                            # não a adicionamento de vizinho
                            self.worker[i].neighbor_list = self.worker[i].neighbor_list

    #
    def step_interact(self):
        """
        Interacting workers by observing coworkers' behaviors and receiving safety feedback from managers and taking their safety behaviors based on the interaction
        """
        # aqui todos os agentes tem seus vizinhos definidos
        self.get_worker_neighbors()
        # list() cria esse vetor  com o total de trabalhadores de 1 a range()
        random_order = list(
            range(self.total_workers))
        # basicamente embaralha a ordem dos trabalhadores no vetor
        np.random.shuffle(random_order)

        # acredito que este for checa se i pertence a randomover embaralhado e se sim realiza o resto
        for i in random_order:

            # random.betavariate(alpha,bbeta) segue o conceito :https://en.wikipedia.org/wiki/Beta_distribution
            # site é 0.5 enta (2,5; 2,5) então h-a uma probabilidade maior de ser sorteado os perto do centro e um pouco pra baixo entre 0 e 1
            if self.worker[i].crew_type == 2:
                self.worker[i].actual_risk = random.betavariate( 10 * self.activity_risk
                    ,4.5-5*self.activity_risk)
            else:
                self.worker[i].actual_risk = random.betavariate(
                    5 * self.activity_risk, 5-5*self.activity_risk)

            # para sabermos se o agente iria entrar em contato com perigo
            self.worker[i].hazard_detection()

            # If a worker is in a safe condition, the worker will not perform an unsafe behavior
            if self.worker[i].unsafe_condition == 0:  # NÃO ESTA EM PERIGO
                # Como há perigos em situações seguras temos que fazer esse if:
                # error_rate = 0.01 que é um numero bem baixo, então a probabilidade de um acidente acotecer numa situação segura é bem baixo
                if np.random.uniform(0, 1) < self.error_rate:
                    self.worker[i].unsafe_behavior = 2  # mistakes
                    # vemos se ele vai se safar do erro =1
                    self.worker[i].near_miss_occurrence()
                    if self.worker[i].near_miss == 1:
                        self.worker[i].attitude_change = - \
                            self.arousal_rate  # arousal_rate  =0,20
                    else:
                        self.worker[i].attitude_change = 0
                    # cada agente começa com um risk attitude ente 0.1 e 0.9
                    self.worker[i].risk_attitude += self.worker[i].attitude_change

                else:
                    self.worker[i].unsafe_behavior = 0
                    # não entendi o motivo de chamarmos essa função s eo o objetivo dela é complementar o resultado da função que define o risk attitude que aqui não é chamada
                    self.worker[i].near_miss_occurrence()
                    self.worker[i].attitude_change = 0
                    # por isso que attitude change muda tão pouco (varia entre a optimism rate e a arousal rate (0,01 e 0,2) pois ela é somada a risk attitude
                    self.worker[i].risk_attitude += self.worker[i].attitude_change

            # PROCESSO CASO HAJA UMA CONDIÇÃO PERIGOSA
            else:
                self.worker[i].perceiving_risk()

                del self.worker[i].workgroup_behavior[0:len(
                    self.worker[i].workgroup_behavior)]

                # The worker will observe the neighbors' behavior to determine risk acceptance
                # só olha os agentes que participam do vetor de vizinhança do agente
                for j in self.worker[i].neighbor_list:

                    # o vizinho esta numa situação perigosa
                    if self.worker[j].unsafe_condition == 1:
                        # If the neighbor performs a safe behavior, the observed behavior will be between 0 and neighbor's actual risk.
                        if self.worker[j].unsafe_behavior == 0:
                            # observation e a primeira variavel local acho
                            observation = np.random.uniform(
                                0, self.worker[j].actual_risk)
                            # ACHO QUE ERA PRA TER UMA FUNÇÃO APPEND AQUI IGUAL NO ELIF
                        # If the neighbor performs an unsafe behavior, the observed behavior will be between neighbor's actual risk and 1.
                        elif self.worker[j].unsafe_behavior == 1:
                            observation = np.random.uniform(
                                self.worker[j].actual_risk, 1)
                            self.worker[i].workgroup_behavior.append(
                                observation)
                        else:
                            print(self.worker[j].unsafe_behavior, "= error")
                    # If the worker is under a safe condition, the worker will not observe the neighbors
                    else:
                        self.worker[i].workgroup_behavior = self.worker[i].workgroup_behavior

                # self.worker[i].perceiving_workgroup_norm()
                self.worker[i].perceiving_management_norm()
                self.worker[i].determining_risk_acceptance()
                self.worker[i].decision_making()
                self.worker[i].receiving_manager_feedback()
                self.worker[i].updating_manager_standard()
                self.worker[i].near_miss_occurrence()
                self.worker[i].updating_risk_attitude()
            self.worker[i].updating_risk_attitude_2()
            self.worker[i].determining_risk_acceptance()

    # todas as funçoes a seguir tirando a ultima são apara tirar a media entre todos os workers dos seus respectivos dados
    @staticmethod
    def get_avg_risk_perception(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.perceived_risk
        return total / len(self.worker)

    @staticmethod
    def get_unsafe_behavior(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                if worker.unsafe_behavior == 1 or worker.unsafe_behavior == 2:
                    total += 1
                else:
                    total = total
        return total

    @staticmethod
    def get_near_miss(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.near_miss
        return total

    @staticmethod
    def get_avg_risk_attitude(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_attitude
        return total / len(self.worker)

    @staticmethod
    def get_avg_risk_acceptance(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_acceptance
        return total / len(self.worker)
 # TIVE QUE REPETIR POIS ACHO QUE QUANDO USA STATIC METOD PODE DE ALGUM ERRO

    def get_avg_risk_perception_2(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.perceived_risk
        return total / len(self.worker)

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
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_attitude
        return total / len(self.worker)

    def get_avg_risk_acceptance_2(self):
        total = 0
        for worker in self.worker:
            if worker.crew_type != 3:
                total += worker.risk_acceptance
        return total / len(self.worker)

    def info_matrix(self):
        matrix = np.array([self.history_near_miss, self.history_near_miss_parede, self.history_near_miss_plataforma,
                           self.history_near_miss_montadores, self.history_near_miss_outros, self.history_risk_attitude,
                           self.history_risk_acceptance, self.history_perceived_risk])
        return matrix

    def incident_rate(self):
        total_near_miss = sum(self.history_near_miss)
        total_working_hour = (
            self.nsteps)*(self.total_workers)*8
        return (total_near_miss/total_working_hour)*(200000/10)

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

    def export(self):
        # criando o DataFrame com os arrays
        df = pd.DataFrame({'history_near_miss': self.history_near_miss,
                           'history_near_miss_parede': self.history_near_miss_parede,
                           'history_near_miss_plataforma': self.history_near_miss_plataforma,
                           'history_near_miss_montadores': self.history_near_miss_montadores,
                           'history_near_miss_outros': self.history_near_miss_outros,
                           'history_risk_attitude': self.history_risk_attitude,
                           'history_risk_acceptance': self.history_risk_acceptance,
                           'history_perceived_risk': self.history_perceived_risk})

        # exportando o DataFrame para um arquivo CSV
        df.to_csv('gerencial_mesa_dados.csv', index=False)

    def step(self):

        self.step_interact()
        #  MESA COLLECTORS
        self.datacollector_risk.collect(self)
        self.datacollector_behavior.collect(self)

        # ARRAYS PARA OUTROS GRÁFICOS

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

        self.t = self.t+1
        # print(self.t)

        if self.t - 2 == self.nsteps:
            self.export()
            self.running = False
        return
