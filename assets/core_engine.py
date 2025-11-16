# core_engine.py
from .fuzzy_module import calcular_macros
from .fuzzy_module.calcular_vet import calculo_valor_energetico_total
from .genetic_module.genetic_module import gerar_cardapio

def _rotular_dieta(objetivo: int, c_perc: float, p_perc: float, g_perc: float):
    # rótulo calórico
    tipo = {0: "hipocalórica", 1: "normocalórica", 2: "hipercalórica"}.get(objetivo, "normocalórica")
    # rótulos por macro
    tags = []
    if c_perc >= 55: tags.append("alto carboidrato")
    if p_perc >= 25: tags.append("alta proteína")
    if g_perc >= 35: tags.append("maior teor de gorduras boas")
    return tipo, tags

def gerar_plano_para_usuario(dados: dict) -> dict:
    """
    dados = {
      "objetivo": 0|1|2,
      "atividade": 0..10,
      "colesterol": 0..300,
      "peso": float,
      "n_refeicoes": 5,
      "restricoes": {"banidos": ["lactose"]},
      "orcamento_max": 30.0,
      "tabela_csv": "data/taco_min.csv",
      "ag": {"pop": 100, "ger": 120, "elit": 6}
    }
    """
    objetivo = int(dados["objetivo"])
    atividade = int(dados["atividade"])
    colesterol = int(dados["colesterol"])
    peso = float(dados["peso"])

    # Fuzzy → metas em gramas e VET
    carb_g, prot_g, fat_g = calcular_macros(objetivo, atividade, colesterol, peso, debug=False)
    vet = calculo_valor_energetico_total(objetivo, peso)

    # Percentuais úteis ao rótulo
    c_kcal = carb_g * 4
    p_kcal = prot_g * 4
    g_kcal = fat_g * 9
    total_kcal = max(1, c_kcal + p_kcal + g_kcal)
    c_perc = c_kcal / total_kcal * 100
    p_perc = p_kcal / total_kcal * 100
    g_perc = g_kcal / total_kcal * 100
    tipo, tags = _rotular_dieta(objetivo, c_perc, p_perc, g_perc)

    # Targets pro AG
    targets = {"kcal": vet, "carb_g": carb_g, "prot_g": prot_g, "fat_g": fat_g}
    params = {
        "n_refeicoes": int(dados.get("n_refeicoes", 5)),
        "restricoes": dados.get("restricoes", {}),
        "orcamento_max": float(dados.get("orcamento_max", 9999)),
        "tabela_csv": dados["tabela_csv"],
        **dados.get("ag", {})
    }
    sol = gerar_cardapio(targets, params)

    # Texto amigável pro chatbot
    resumo = (
        f"Plano {tipo}, " +
        (", ".join(tags) + ", " if tags else "") +
        f"para {peso:.1f} kg: ~{vet:.0f} kcal/dia. Metas: "
        f"CHO {carb_g} g, PRO {prot_g} g, GORD {fat_g} g."
    )

    return {
      "resumo": resumo,
      "alvos": {"vet": vet, **targets, "perc": {"carb": c_perc, "prot": p_perc, "gord": g_perc}},
      "cardapio": sol["refeicoes"],
      "metricas": sol["fitness"],
      "historico_otimizacao": sol["historico"],
    }
