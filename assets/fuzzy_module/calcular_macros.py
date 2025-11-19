# assets/fuzzy_module/calcular_macros.py
"""
Módulo: calcular_macros
-----------------------

Responsável por gerar as metas de carboidratos, proteínas e gorduras
utilizando **Lógica Fuzzy**, a partir de três variáveis principais:

- Objetivo (cutting, manutenção, bulking)
- Atividade física (0 a 10)
- Colesterol (mg/dL)

O resultado são percentuais de distribuição de macronutrientes (% CHO, % PRO, % FAT),
que depois são convertidos em gramas com base no VET (Valor Energético Total).

(Por que usamos funções **triangulares**? → A função triangular `trimf`
é simples, eficiente, fácil de interpretar e amplamente usada em Fuzzy Systems.
Ela permite transições suaves entre categorias linguísticas, sem gerar efeitos
abruptos. Ideal para sistemas com baixa complexidade, baixo custo computacional
e onde queremos regras claras e visualmente compreensíveis.)
"""

# ---------------------------------------------------------------------------
# Comentários e ajustes inseridos com auxílio do ChatGPT (GPT-5.1 Thinking)
# Data: 2025-11-19
# ---------------------------------------------------------------------------

from skfuzzy import control as ctrl
from .calcular_vet import calculo_valor_energetico_total
import numpy as np
import skfuzzy as fuzz


# ============================================================================
# DEFINIÇÃO DOS UNIVERSOS LINGUÍSTICOS
# ============================================================================

# Antecedentes (variáveis de entrada)
objetivo   = ctrl.Antecedent(np.arange(1, 3, 1), "objetivo")       # 0=CUT, 1=MAN, 2=BULK
atividade  = ctrl.Antecedent(np.arange(1, 11, 1), "atividade")     # 0..10
colesterol = ctrl.Antecedent(np.arange(1, 301, 1), "colesterol")   # mg/dL

# Consequentes (variáveis de saída – percentuais)
carbo    = ctrl.Consequent(np.arange(40, 71, 1), "carbo")         # %
proteina = ctrl.Consequent(np.arange(15, 31, 1), "proteina")      # %
gordura  = ctrl.Consequent(np.arange(15, 46, 1), "gordura")       # %


# ============================================================================
# FUNÇÕES DE PERTINÊNCIA (triangulares)
# ============================================================================
# (trimf é usada aqui por clareza, eficiência e transições suaves entre rótulos)

# Objetivo
objetivo["cutting"]    = fuzz.trimf(objetivo.universe, [0, 0, 1])
objetivo["manutencao"] = fuzz.trimf(objetivo.universe, [0, 1, 2])
objetivo["bulking"]    = fuzz.trimf(objetivo.universe, [1, 2, 2])

# Atividade física
atividade["baixa"]     = fuzz.trimf(atividade.universe,  [0, 3, 6])
atividade["moderada"]  = fuzz.trimf(atividade.universe,  [3, 6, 9])
atividade["alta"]      = fuzz.trimf(atividade.universe,  [6, 9, 11])

# Colesterol
colesterol["baixo"] = fuzz.trimf(colesterol.universe, [0, 120, 150])
colesterol["medio"] = fuzz.trimf(colesterol.universe, [120, 150, 220])
colesterol["alto"]  = fuzz.trimf(colesterol.universe, [150, 200, 250])

# Macronutrientes
carbo["baixo"]  = fuzz.trimf(carbo.universe, [40, 45, 55])
carbo["medio"]  = fuzz.trimf(carbo.universe, [45, 55, 65])
carbo["alto"]   = fuzz.trimf(carbo.universe, [55, 65, 70])

proteina["baixa"] = fuzz.trimf(proteina.universe, [15, 18, 21])
proteina["media"] = fuzz.trimf(proteina.universe, [18, 21, 25])
proteina["alta"]  = fuzz.trimf(proteina.universe, [21, 25, 29])

gordura["baixa"] = fuzz.trimf(gordura.universe, [15, 20, 25])
gordura["media"] = fuzz.trimf(gordura.universe, [20, 25, 35])
gordura["alta"]  = fuzz.trimf(gordura.universe, [25, 35, 45])


# ============================================================================
# REGRAS FUZZY
# ============================================================================

regras = [
    # -------------------------------
    # OBJETIVO: CUTTING
    # -------------------------------
    # atividade BAIXA
    ctrl.Rule(objetivo["cutting"] & atividade["baixa"] & colesterol["baixo"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["baixa"] & colesterol["medio"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["baixa"] & colesterol["alto"],
              (carbo["baixo"], proteina["alta"], gordura["baixa"])),

    # atividade MODERADA
    ctrl.Rule(objetivo["cutting"] & atividade["moderada"] & colesterol["baixo"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["moderada"] & colesterol["medio"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["moderada"] & colesterol["alto"],
              (carbo["baixo"], proteina["alta"], gordura["baixa"])),

    # atividade ALTA
    ctrl.Rule(objetivo["cutting"] & atividade["alta"] & colesterol["baixo"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["alta"] & colesterol["medio"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["cutting"] & atividade["alta"] & colesterol["alto"],
              (carbo["baixo"], proteina["alta"], gordura["baixa"])),

    # -------------------------------
    # OBJETIVO: MANUTENÇÃO
    # -------------------------------
    # atividade BAIXA
    ctrl.Rule(objetivo["manutencao"] & atividade["baixa"] & colesterol["baixo"],
              (carbo["medio"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["baixa"] & colesterol["medio"],
              (carbo["medio"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["baixa"] & colesterol["alto"],
              (carbo["baixo"], proteina["media"], gordura["baixa"])),

    # atividade MODERADA
    ctrl.Rule(objetivo["manutencao"] & atividade["moderada"] & colesterol["baixo"],
              (carbo["medio"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["moderada"] & colesterol["medio"],
              (carbo["medio"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["moderada"] & colesterol["alto"],
              (carbo["medio"], proteina["media"], gordura["baixa"])),

    # atividade ALTA
    ctrl.Rule(objetivo["manutencao"] & atividade["alta"] & colesterol["baixo"],
              (carbo["alto"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["alta"] & colesterol["medio"],
              (carbo["alto"], proteina["media"], gordura["media"])),
    ctrl.Rule(objetivo["manutencao"] & atividade["alta"] & colesterol["alto"],
              (carbo["medio"], proteina["media"], gordura["media"])),

    # -------------------------------
    # OBJETIVO: BULKING
    # -------------------------------
    # atividade BAIXA
    ctrl.Rule(objetivo["bulking"] & atividade["baixa"] & colesterol["baixo"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["bulking"] & atividade["baixa"] & colesterol["medio"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["bulking"] & atividade["baixa"] & colesterol["alto"],
              (carbo["medio"], proteina["alta"], gordura["baixa"])),

    # atividade MODERADA
    ctrl.Rule(objetivo["bulking"] & atividade["moderada"] & colesterol["baixo"],
              (carbo["alto"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["bulking"] & atividade["moderada"] & colesterol["medio"],
              (carbo["medio"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["bulking"] & atividade["moderada"] & colesterol["alto"],
              (carbo["medio"], proteina["alta"], gordura["baixa"])),

    # atividade ALTA
    ctrl.Rule(objetivo["bulking"] & atividade["alta"] & colesterol["baixo"],
              (carbo["alto"], proteina["alta"], gordura["alta"])),
    ctrl.Rule(objetivo["bulking"] & atividade["alta"] & colesterol["medio"],
              (carbo["alto"], proteina["alta"], gordura["media"])),
    ctrl.Rule(objetivo["bulking"] & atividade["alta"] & colesterol["alto"],
              (carbo["medio"], proteina["alta"], gordura["baixa"])),
]

# Sistema de controle fuzzy
nutri_ctrl = ctrl.ControlSystem(regras)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def _clamp(v, lo, hi):
    """Limita o valor v ao intervalo [lo, hi]."""
    return max(lo, min(hi, v))


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================
def calcular_macros(
    objetivo_in: int,
    atividade_in: int,
    colesterol_in: int,
    peso: float,
    debug: bool = False,
) -> tuple[int, int, int]:
    """
    Calcula as metas de macronutrientes (g/dia) usando Lógica Fuzzy.

    Retorna:
        (carboidratos_g, proteina_g, gordura_g)
    """

    # ------------------------------
    # Sanitização da entrada
    # ------------------------------
    objetivo_in   = int(_clamp(objetivo_in, 0, 2))
    atividade_in  = int(_clamp(atividade_in, 0, 10))
    colesterol_in = int(_clamp(colesterol_in, 0, 300))

    assert peso > 0, "Peso deve ser > 0"

    # ------------------------------
    # Executa simulação fuzzy
    # ------------------------------
    sim = ctrl.ControlSystemSimulation(nutri_ctrl)

    sim.input["objetivo"]   = objetivo_in
    sim.input["atividade"]  = atividade_in
    sim.input["colesterol"] = colesterol_in

    sim.compute()

    # Saídas (em porcentagem do VET)
    c_perc = float(sim.output["carbo"])
    p_perc = float(sim.output["proteina"])
    g_perc = float(sim.output["gordura"])

    # ------------------------------
    # Normalização — soma deve ser 100%
    # ------------------------------
    total = c_perc + p_perc + g_perc
    c_perc, p_perc, g_perc = (x / total * 100 for x in (c_perc, p_perc, g_perc))

    # ------------------------------
    # Conversão para gramas
    # ------------------------------
    vet = calculo_valor_energetico_total(objetivo_in, peso)

    cho_g = round((vet * (c_perc / 100)) / 4)  # 4 kcal por grama de carbo
    pro_g = round((vet * (p_perc / 100)) / 4)  # 4 kcal por grama de proteína
    fat_g = round((vet * (g_perc / 100)) / 9)  # 9 kcal por grama de gordura

    # ------------------------------
    # Debug visual opcional
    # ------------------------------
    if debug:
        try:
            import matplotlib.pyplot as plt
            carbo.view(sim=sim)
            proteina.view(sim=sim)
            gordura.view(sim=sim)
            plt.show()
        except Exception:
            pass

    return cho_g, pro_g, fat_g
