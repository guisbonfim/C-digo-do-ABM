
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import  Slider, Choice
# from mesa.time import RandomActivation
from gerencial_a import Model


simulation_params = {

    "num_crews_1": Slider(
        "Número de equipes de montadores",
        1, 0, 10,
        description='Quantidade de equipes ',
        step=1,),

    "num_worker_per_crew_1": Slider(
        "Número de trabalhadores por equipe",
        21, 1, 25,
        description='Trabalhadores por equipe ',
        step=1,),
    "num_crews_2": Slider(
        "Número de equipes de montadores de plataformas",
        1, 0, 10,
        description='Quantidade de equipes ',
        step=1,),

    "num_worker_per_crew_2": Slider(
        "Número de trabalhadores por equipe",
        7, 1, 20,
        description='Trabalhadores por equipe de montagem de plataforma',
        step=1,),

    "num_other_workers": Slider(
        "Número de colaboradores da construção civil",
        12, 0, 100,
        description='Trabalhadores no canteiro que não são montadores',
        step=1,),

    "n_steps": Slider(
        "Tempo de duração da obra (Dias)",
        900, 30, 1000,
        description='Número de steps ',
        step=30,),

    "activity_risk": Slider(
        "Taxa de risco da atividade",
        0.5, 0.1, 1,
        description='Porcentagem do perigo no canteiro',
        step=0.1,),


    "freq_reun": Choice( 'Regularidade dos diálogos de segurança', value='Daily',
                                       choices=['Daily', 'Weekly']),

    "freq_trein_1": Slider(
        "Regularidade dos TreinamentoS de riscos gerais (NR-18)",
        2, 1, 12,
        description='Quantidade de treinamentos por ano dos montadores',
        step=1,
    ),
    
    "freq_trein_2": Slider(
        "Regularidade dos Treinamento de atividades em altura (NR-35)",
        2, 1, 12,
        description='Quantidade de treinamentos por ano dos montadores',
        step=1,
    ),
    "feedback_frequency": Slider(
        "Rigor de feedback",
        0.7, 0.1, 1,
        description='Frequência de feedback',
        step=0.1,
    ),

    "using_mesa": Slider(
        "NÃO MEXER",
        1, 1, 1,
        description='XXX',
        step=1,
    ),

    # "Priori":UserSettableParameter(
    #    "choice",
    #    "Priorização de intervenção na comunidade",
    #    value='Sem priorização',
    #    choices="['Sem priorização','Casas de pior estrutura','Casas de melhor estrutura']",
    #    description='Priorização do das intevenções',
    #    step=1,
    # ),
    # OLHAR COMO ERA ANTES POIS MUDEI, ERA UMA VAIRAVEL NUMBER CELL
}


chart_risk = ChartModule(
    [
        # {"Label": "Risk Attitude Average", "Color": "green"},
        {"Label": "Average Risk Tolerance", "Color": "blue"},
    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_risk"
)
chart_perception = ChartModule(
    [
        {"Label": "Average Risk Perception", "Color": "red"},
    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_risk"
)
chart_behavior = ChartModule(
    [
        {"Label": "Unsafe Behaviors", "Color": "orange"},

    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_behavior"
)
chart_behavior2 = ChartModule(
    [
        {"Label": "Near Misses", "Color": "blue"},

    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_behavior"
)

server = ModularServer(Model,
                       [chart_risk, chart_perception,
                           chart_behavior, chart_behavior2],
                       'Model',
                       simulation_params
                       )
server.port = 8521
server.launch()
