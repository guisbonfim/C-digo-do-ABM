

from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from gerencial_a import Model


simulation_params = {

    "num_crews_1": UserSettableParameter(
        "slider",
        "Número de equipes de montadores",
        1, 0, 10,
        description='Quantidade de equipes ',
        step=1,
    ),

    "num_worker_per_crew_1": UserSettableParameter(
        "slider",
        "Número de trabalhadores por equipe de montadores",
        10, 1, 20,
        description='Trabalhadores por equipe ',
        step=1,
    ),

    "num_crews_2": UserSettableParameter(
        "slider",
        "Número de equipes de montadores de plataformas",
        1, 0, 10,
        description='Quantidade de equipes ',
        step=1,
    ),

    "num_worker_per_crew_2": UserSettableParameter(
        "slider",
        "Número de trabalhadores por equipe de plataforma",
        10, 1, 20,
        description='Trabalhadores por equipe de montagem de plataforma',
        step=1,
    ),

    "num_other_workers": UserSettableParameter(
        "slider",
        "Número de outros trbalhadores que não são montadores",
        1, 0, 100,
        description='Trabalhadores no canteiro que não são montadores',
        step=1,
    ),

    "n_steps": UserSettableParameter(
        "slider",
        "Tempo de duração da obra (Dias)",
        30, 30, 900,
        description='Número de steps ',
        step=30,
    ),

    "activity_risk": UserSettableParameter(
        "slider",
        "Taxa de risco da atividade",
        0.5, 0.1, 1,
        description='Porcentagem do perigo no canteiro',
        step=0.1,
    ),


    "freq_reun": UserSettableParameter(
        'choice', 
        'Regularidade dos diálogos de segurança', 
        value='Diário',
        choices=['Diário', 'Semanal']
    ),

    "freq_trein_1": UserSettableParameter(
        "choice",
        "Regularidade dos treinamentos de segurança (em meses)",
        value=12,
        choices=[3, 6, 12, 24],
        description='Quantidade de treinamentos por ano dos montadores',
    ),
    
    "feedback_frequency": UserSettableParameter(
        "choice",
        "Rigor de feedback",
        value=0.5,
        choices=[0.3, 0.5, 0.7],
        description='Frequência de feedback',
    ),
}


chart_risk = ChartModule(
    [
        {"Label": "Média de Tolerância ao Risco", "Color": "blue"},
    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_risk"
)
chart_perception = ChartModule(
    [
        {"Label": "Média de Percepção de Risco", "Color": "red"},
    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_risk"
)
chart_behavior = ChartModule(
    [
        {"Label": "Comportamentos Inseguros", "Color": "orange"},

    ],
    canvas_height=200,
    canvas_width=500,
    data_collector_name="datacollector_behavior"
)
chart_behavior2 = ChartModule(
    [
        {"Label": "Quase Acidentes", "Color": "purple"},

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
