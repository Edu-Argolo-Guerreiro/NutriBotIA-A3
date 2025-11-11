import numpy as np
from skfuzzy import control as ctrl

renda_univ = np.arange(0, 11, 1)
tempo_univ = np.arange(0, 11, 1)
saude_univ = np.arange(0, 11, 1)
prioridade_univ = np.arange(0, 11, 1)

renda = ctrl.Antecedent(renda_univ, "renda")
tempo_cozinha = ctrl.Antecedent(tempo_univ, "tempo_cozinha")
saude_geral = ctrl.Antecedent(saude_univ, "saude_geral")
prioridade_nutricional = ctrl.Consequent(prioridade_univ, "prioridade_nutricional")
