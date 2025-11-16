# assets/fuzzy_module/calcular_macros.py
from skfuzzy import control as ctrl
from .calcular_vet import calculo_valor_energetico_total
import numpy as np
import skfuzzy as fuzz

# Universos
objetivo = ctrl.Antecedent(np.arange(0, 3, 1), "objetivo")      # 0=CUT,1=MAN,2=BULK
atividade = ctrl.Antecedent(np.arange(0, 11, 1), "atividade")   # 0..10
colesterol = ctrl.Antecedent(np.arange(0, 301, 1), "colesterol")# mg/dL

# Consequentes (em %)
carbo = ctrl.Consequent(np.arange(40, 71, 1), "carbo")
proteina = ctrl.Consequent(np.arange(15, 31, 1), "proteina")
gordura = ctrl.Consequent(np.arange(15, 46, 1), "gordura")

# Pertinências
objetivo["cutting"]    = fuzz.trimf(objetivo.universe, [0, 0, 1])
objetivo["manutencao"] = fuzz.trimf(objetivo.universe, [0, 1, 2])
objetivo["bulking"]    = fuzz.trimf(objetivo.universe, [1, 2, 2])

atividade["baixa"]     = fuzz.trimf(atividade.universe, [0, 3, 6])
atividade["moderada"]  = fuzz.trimf(atividade.universe, [3, 6, 9])
atividade["alta"]      = fuzz.trimf(atividade.universe, [6, 9, 11])

colesterol["baixo"] = fuzz.trimf(colesterol.universe, [0, 120, 150])
colesterol["medio"] = fuzz.trimf(colesterol.universe, [120, 150, 220])
colesterol["alto"]  = fuzz.trimf(colesterol.universe, [150, 200, 250])

carbo["baixo"]  = fuzz.trimf(carbo.universe, [40, 45, 55])
carbo["medio"]  = fuzz.trimf(carbo.universe, [45, 55, 65])
carbo["alto"]   = fuzz.trimf(carbo.universe, [55, 65, 70])

proteina["baixa"] = fuzz.trimf(proteina.universe, [15, 18, 21])
proteina["media"] = fuzz.trimf(proteina.universe, [18, 21, 25])
proteina["alta"]  = fuzz.trimf(proteina.universe, [21, 25, 29])

gordura["baixa"] = fuzz.trimf(gordura.universe, [15, 20, 25])
gordura["media"] = fuzz.trimf(gordura.universe, [20, 25, 35])
gordura["alta"]  = fuzz.trimf(gordura.universe, [25, 35, 45])

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

def _clamp(v, lo, hi): return max(lo, min(hi, v))

def calcular_macros(objetivo_in: int, atividade_in: int, colesterol_in: int, peso: float,
                    debug: bool=False) -> tuple[int, int, int]:
    # Sanitização
    objetivo_in  = int(_clamp(objetivo_in, 0, 2))
    atividade_in = int(_clamp(atividade_in, 0, 10))
    colesterol_in= int(_clamp(colesterol_in, 0, 300))
    assert peso > 0, "Peso deve ser > 0"

    # Recria a simulação a cada chamada
    sim = ctrl.ControlSystemSimulation(nutri_ctrl)

    sim.input["objetivo"] = objetivo_in
    sim.input["atividade"] = atividade_in
    sim.input["colesterol"] = colesterol_in
    sim.compute()

    c_perc = float(sim.output["carbo"])
    p_perc = float(sim.output["proteina"])
    g_perc = float(sim.output["gordura"])

    # Normalização (garante soma = 100)
    total = c_perc + p_perc + g_perc
    c_perc, p_perc, g_perc = (x/total*100 for x in (c_perc, p_perc, g_perc))

    vet = calculo_valor_energetico_total(objetivo_in, peso)

    cho_g = round((vet * (c_perc/100)) / 4)
    pro_g = round((vet * (p_perc/100)) / 4)
    fat_g = round((vet * (g_perc/100)) / 9)

    if debug:
        try:
            import matplotlib.pyplot as plt
            carbo.view(sim=sim); proteina.view(sim=sim); gordura.view(sim=sim); plt.show()
        except Exception:
            pass

    return cho_g, pro_g, fat_g
