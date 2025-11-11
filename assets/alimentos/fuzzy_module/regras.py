import skfuzzy as fuzz
from skfuzzy import control as ctrl
from .constantes import *   # <- COM ponto

# Definição das Funções de Pertinência

# Renda
renda["baixa"] = fuzz.trimf(renda_univ, [0, 0, 4])
renda["media"] = fuzz.trimf(renda_univ, [2, 5, 8])
renda["alta"] = fuzz.trimf(renda_univ, [6, 10, 10])

# Tempo de Cozinha
tempo_cozinha["pouco"] = fuzz.trimf(tempo_univ, [0, 0, 4])
tempo_cozinha["medio"] = fuzz.trimf(tempo_univ, [2, 5, 8])
tempo_cozinha["muito"] = fuzz.trimf(tempo_univ, [6, 10, 10])

# Saúde Geral
saude_geral["delicada"] = fuzz.trimf(saude_univ, [0, 0, 4])
saude_geral["ok"] = fuzz.trimf(saude_univ, [2, 5, 8])
saude_geral["boa"] = fuzz.trimf(saude_univ, [6, 10, 10])

# Prioridade Nutricional
prioridade_nutricional["baixa"] = fuzz.trimf(prioridade_univ, [0, 0, 3])
prioridade_nutricional["media"] = fuzz.trimf(prioridade_univ, [2, 5, 7])
prioridade_nutricional["alta"] = fuzz.trimf(prioridade_univ, [5, 7, 9])
prioridade_nutricional["critica"] = fuzz.trimf(prioridade_univ, [7, 10, 10])

# Definição das Regras Fuzzy
regras = [
    ctrl.Rule(saude_geral["delicada"] & renda["baixa"], prioridade_nutricional["critica"]),
    ctrl.Rule(saude_geral["delicada"] & tempo_cozinha["pouco"], prioridade_nutricional["critica"]),
    ctrl.Rule(saude_geral["delicada"] & renda["media"], prioridade_nutricional["alta"]),
    ctrl.Rule(renda["baixa"] & tempo_cozinha["pouco"], prioridade_nutricional["alta"]),
    ctrl.Rule(saude_geral["ok"] & renda["baixa"], prioridade_nutricional["alta"]),
    ctrl.Rule(saude_geral["ok"] & renda["media"] & tempo_cozinha["medio"], prioridade_nutricional["media"]),
    ctrl.Rule(saude_geral["boa"] & renda["media"] & tempo_cozinha["pouco"], prioridade_nutricional["media"]),
    ctrl.Rule(saude_geral["boa"] & renda["alta"] & tempo_cozinha["muito"], prioridade_nutricional["baixa"]),
    ctrl.Rule(saude_geral["boa"] & renda["alta"], prioridade_nutricional["baixa"]),
    ctrl.Rule(tempo_cozinha["muito"] & renda["alta"], prioridade_nutricional["baixa"])
]

# Montagem do ControlSystem e ControlSystemSimulation
sistema_controle = ctrl.ControlSystem(regras)
simulador_prioridade = ctrl.ControlSystemSimulation(sistema_controle)