# core_engine.py
import os

# Tenta primeiro como pacote (quando o projeto é usado com `python -m ...`)
try:
    from .fuzzy_module import calcular_macros
    from .fuzzy_module.calcular_vet import calculo_valor_energetico_total
    from .genetic_module.genetic_module import gerar_cardapio
except ImportError:
    # Fallback para quando rodamos scripts soltos dentro de assets/
    import sys
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta assets
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)

    from fuzzy_module import calcular_macros
    from fuzzy_module.calcular_vet import calculo_valor_energetico_total
    from genetic_module.genetic_module import gerar_cardapio


def _rotular_dieta(objetivo: int, c_perc: float, p_perc: float, g_perc: float):
    tipo = {0: "hipocalórica", 1: "normocalórica", 2: "hipercalórica"}.get(objetivo, "normocalórica")
    tags = []
    if c_perc >= 55:
        tags.append("alto carboidrato")
    if p_perc >= 25:
        tags.append("alta proteína")
    if g_perc >= 35:
        tags.append("maior teor de gorduras boas")
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
      "tabela_csv": "data/taco_min.csv" OU "assets/data/taco_min.csv" OU caminho absoluto,
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

    # ---------- resolver caminho da tabela CSV de forma robusta ----------
    base_assets = os.path.dirname(os.path.abspath(__file__))  # pasta assets
    tabela_csv_raw = dados.get("tabela_csv", "data/taco_min.csv")

    # se já for caminho absoluto, usa direto
    if os.path.isabs(tabela_csv_raw):
        tabela_csv = tabela_csv_raw
    else:
        # se vier "assets/data/taco_min.csv", remove o prefixo "assets/"
        if tabela_csv_raw.startswith("assets/") or tabela_csv_raw.startswith("assets\\"):
            tabela_csv_raw = tabela_csv_raw.split("assets/", 1)[-1].split("assets\\", 1)[-1]
        # junta com a pasta assets
        tabela_csv = os.path.join(base_assets, tabela_csv_raw)
    # ---------------------------------------------------------------------

    # Targets pro AG
    targets = {"kcal": vet, "carb_g": carb_g, "prot_g": prot_g, "fat_g": fat_g}
    params = {
        "n_refeicoes": int(dados.get("n_refeicoes", 5)),
        "restricoes": dados.get("restricoes", {}),
        "orcamento_max": float(dados.get("orcamento_max", 9999)),
        "tabela_csv": tabela_csv,
        **dados.get("ag", {})
    }
    sol = gerar_cardapio(targets, params)

    resumo = (
        f"Plano {tipo}, "
        + (", ".join(tags) + ", " if tags else "")
        + f"para {peso:.1f} kg: ~{vet:.0f} kcal/dia. Metas: "
        f"CHO {carb_g} g, PRO {prot_g} g, GORD {fat_g} g."
    )

    return {
        "resumo": resumo,
        "alvos": {
            "vet": vet,
            **targets,
            "perc": {"carb": c_perc, "prot": p_perc, "gord": g_perc},
        },
        "cardapio": sol["refeicoes"],
        "metricas": sol["fitness"],
        "historico_otimizacao": sol["historico"],
    }
