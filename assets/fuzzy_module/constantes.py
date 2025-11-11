import numpy as np
from skfuzzy import control as ctrl

# Definição dos Universos de Discurso (0 a 10)

# Entradas (Antecedentes)
renda_univ = np.arange(0, 11, 1)
tempo_univ = np.arange(0, 11, 1)
saude_univ = np.arange(0, 11, 1)

# Saída (Consequente)
prioridade_univ = np.arange(0, 11, 1)

# Criação das Variáveis Fuzzy (Antecedent e Consequent)
renda = ctrl.Antecedent(renda_univ, "renda")
tempo_cozinha = ctrl.Antecedent(tempo_univ, "tempo_cozinha")
saude_geral = ctrl.Antecedent(saude_univ, "saude_geral")
prioridade_nutricional = ctrl.Consequent(prioridade_univ, "prioridade_nutricional")