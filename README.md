# Projeto de Pesquisa: ABM - Modelagem Baseada Em Agentes

Este repositório contém um modelo de simulação baseado na biblioteca [Mesa](https://mesa.readthedocs.io/en/stable/) para estudar o comportamento de trabalhadores em um ambiente de trabalho representando o campo da construção civil de paredes de concreto, com foco nos montadores de andaimes e montadores de parede de concreto. O modelo simula a dinâmica entre trabalhadores e suas atitudes em relação ao risco, condições de trabalho e intervenções gerenciais, e abre a possibilidade de simular diversas ações gerenciais para avaliar o impacto dentro do canteiro de obras.

## Principais Componentes

- **`Worker`**: Representa um trabalhador no canteiro de obras, com atributos como atitude em relação ao risco, percepção de risco e comportamento inseguro.
- **`Model`**: Define o ambiente da simulação, configura os trabalhadores e controla a execução dos passos da simulação.

## Dependências

Para rodar o código, você precisará das seguintes bibliotecas Python:

- `mesa`
- `numpy`
- `pandas`
- `seaborn`

Você pode instalar as dependências usando o `pip`:

```bash
pip install mesa numpy pandas seaborn
