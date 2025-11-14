from skfuzzy import control as ctrl
from .calcular_vet import calculo_valor_energetico_total
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz

# Objetivo corporal: 0=cutting, 1=manutenção, 2=bulking
objetivo = ctrl.Antecedent(np.arange(0, 3, 1), "objetivo")
# Nível de atividade física: 0 - 2 sedentário, 3 - 4 exercício leve, 5 - 6 exercício moderado, 7 - 8 exercício pesado, 9 - 10 atleta
atividade = ctrl.Antecedent(np.arange(0, 11, 1), "atividade")
# colesterol
colesterol = ctrl.Antecedent(np.arange(0, 301, 1), "colesterol")  # A definir mg/dl

# Macronutrientes em g/kg
carbo = ctrl.Consequent(np.arange(40, 80, 1), "carbo")  # Carboidratos porcentagem
proteina = ctrl.Consequent(np.arange(10, 35, 1), "proteina")  # Proteínas %
gordura = ctrl.Consequent(np.arange(15, 46, 1), "gordura")  # Gorduras %

# Funções de pertinência para as entradas
objetivo["cutting"] = fuzz.trimf(objetivo.universe, [0, 0, 1])
objetivo["manutencao"] = fuzz.trimf(objetivo.universe, [0, 1, 2])
objetivo["bulking"] = fuzz.trimf(objetivo.universe, [1, 2, 2])

# Atividade
atividade["baixa"] = fuzz.trimf(atividade.universe, [0, 3, 6])
atividade["moderada"] = fuzz.trimf(atividade.universe, [3, 6, 9])
atividade["alta"] = fuzz.trimf(atividade.universe, [6, 9, 11])

# colesterol
colesterol["baixo"] = fuzz.trimf(colesterol.universe, [0, 120, 150])
colesterol["medio"] = fuzz.trimf(colesterol.universe, [120, 150, 220])
colesterol["alto"] = fuzz.trimf(colesterol.universe, [150, 200, 250])

# Carboidratos %
carbo["baixo"] = fuzz.trimf(carbo.universe, [40, 45, 55])
carbo["medio"] = fuzz.trimf(carbo.universe, [45, 55, 65])
carbo["alto"] = fuzz.trimf(carbo.universe, [55, 65, 70])

# Proteínas %
proteina["baixa"] = fuzz.trimf(proteina.universe, [15, 18, 21])
proteina["media"] = fuzz.trimf(proteina.universe, [18, 21, 25])
proteina["alta"] = fuzz.trimf(proteina.universe, [21, 25, 29])

# Gorduras %
gordura["baixa"] = fuzz.trimf(gordura.universe, [15, 20, 25])
gordura["media"] = fuzz.trimf(gordura.universe, [20, 25, 35])
gordura["alta"] = fuzz.trimf(gordura.universe, [25, 35, 45])

regras = [
    # ==========================================================
    # OBJETIVO: CUTTING
    # ==========================================================
    # Cutting + atividade BAIXA
    ctrl.Rule(
        objetivo["cutting"] & atividade["baixa"] & colesterol["baixo"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["baixa"] & colesterol["medio"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["baixa"] & colesterol["alto"],
        (carbo["baixo"], proteina["alta"], gordura["baixa"]),
    ),
    # Cutting + atividade MODERADA
    ctrl.Rule(
        objetivo["cutting"] & atividade["moderada"] & colesterol["baixo"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["moderada"] & colesterol["medio"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["moderada"] & colesterol["alto"],
        (carbo["baixo"], proteina["alta"], gordura["baixa"]),
    ),
    # Cutting + atividade ALTA
    ctrl.Rule(
        objetivo["cutting"] & atividade["alta"] & colesterol["baixo"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["alta"] & colesterol["medio"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["cutting"] & atividade["alta"] & colesterol["alto"],
        (carbo["baixo"], proteina["alta"], gordura["baixa"]),
    ),
    # ==========================================================
    # OBJETIVO: MANUTENÇÃO
    # ==========================================================
    # Manutenção + atividade BAIXA
    ctrl.Rule(
        objetivo["manutencao"] & atividade["baixa"] & colesterol["baixo"],
        (carbo["medio"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["baixa"] & colesterol["medio"],
        (carbo["medio"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["baixa"] & colesterol["alto"],
        (carbo["baixo"], proteina["media"], gordura["baixa"]),
    ),
    # Manutenção + atividade MODERADA
    ctrl.Rule(
        objetivo["manutencao"] & atividade["moderada"] & colesterol["baixo"],
        (carbo["medio"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["moderada"] & colesterol["medio"],
        (carbo["medio"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["moderada"] & colesterol["alto"],
        (carbo["medio"], proteina["media"], gordura["baixa"]),
    ),
    # Manutenção + atividade ALTA
    ctrl.Rule(
        objetivo["manutencao"] & atividade["alta"] & colesterol["baixo"],
        (carbo["alto"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["alta"] & colesterol["medio"],
        (carbo["alto"], proteina["media"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["manutencao"] & atividade["alta"] & colesterol["alto"],
        (carbo["medio"], proteina["media"], gordura["media"]),
    ),
    # ==========================================================
    # OBJETIVO: BULKING
    # ==========================================================
    # Bulking + atividade BAIXA
    ctrl.Rule(
        objetivo["bulking"] & atividade["baixa"] & colesterol["baixo"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["baixa"] & colesterol["medio"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["baixa"] & colesterol["alto"],
        (carbo["medio"], proteina["alta"], gordura["baixa"]),
    ),
    # Bulking + atividade MODERADA
    ctrl.Rule(
        objetivo["bulking"] & atividade["moderada"] & colesterol["baixo"],
        (carbo["alto"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["moderada"] & colesterol["medio"],
        (carbo["medio"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["moderada"] & colesterol["alto"],
        (carbo["medio"], proteina["alta"], gordura["baixa"]),
    ),
    # Bulking + atividade ALTA
    ctrl.Rule(
        objetivo["bulking"] & atividade["alta"] & colesterol["baixo"],
        (carbo["alto"], proteina["alta"], gordura["alta"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["alta"] & colesterol["medio"],
        (carbo["alto"], proteina["alta"], gordura["media"]),
    ),
    ctrl.Rule(
        objetivo["bulking"] & atividade["alta"] & colesterol["alto"],
        (carbo["medio"], proteina["alta"], gordura["baixa"]),
    ),
]


nutri_ctrl = ctrl.ControlSystem(regras)
nutri_sim = ctrl.ControlSystemSimulation(nutri_ctrl)


# Essa função pega todos os dados necessários do paciente e com o uso da defuzzificação retorna os valores de carboidratos, proteinas e gorduras necessários para o objetivo do paciente
def calcular_macros(
    objetivo: int, atividade: int, colesterol: int, peso: float
) -> tuple:

    valor_energetico_total = calculo_valor_energetico_total(objetivo, peso)

    nutri_sim.input["objetivo"] = objetivo
    nutri_sim.input["atividade"] = atividade
    nutri_sim.input["colesterol"] = colesterol

    nutri_sim.compute()

    carbo_out = nutri_sim.output["carbo"]
    proteina_out = nutri_sim.output["proteina"]
    gordura_out = nutri_sim.output["gordura"]

    total_raw = carbo_out + proteina_out + gordura_out
    carbo_perc = (carbo_out / total_raw) * 100
    proteina_perc = (proteina_out / total_raw) * 100
    gordura_perc = (gordura_out / total_raw) * 100

    # Tirar em produção
    carbo.view(sim=nutri_sim)
    proteina.view(sim=nutri_sim)
    gordura.view(sim=nutri_sim)
    plt.show()

    carboidratos_em_kcal = valor_energetico_total * (carbo_perc / 100)
    proteinas_em_kcal = valor_energetico_total * (proteina_perc / 100)
    gorduras_em_kcal = valor_energetico_total * (gordura_perc / 100)

    carboidratos_em_gramas = round(carboidratos_em_kcal / 4)
    proteinas_em_gramas = round(proteinas_em_kcal / 4)
    gorduras_em_gramas = round(gorduras_em_kcal / 9)

    return carboidratos_em_gramas, proteinas_em_gramas, gorduras_em_gramas
