# core_engine.py
"""
Módulo: core_engine
-------------------

Responsável por orquestrar o fluxo principal do NutriBotIA:

1. Recebe os dados brutos do usuário (objetivo, atividade, colesterol, peso, etc.)
2. Chama o módulo de Lógica Fuzzy para calcular:
   - Metas de macronutrientes (carboidratos, proteínas, gorduras)
   - Valor energético total (VET) diário
3. Configura e aciona o Algoritmo Genético para gerar um cardápio otimizado
4. Rotula o tipo de dieta (hipocalórica, normocalórica, hipercalórica)
   e cria um resumo textual amigável.
"""

# ---------------------------------------------------------------------------
# Comentários e ajustes de revisão inseridos com auxílio do ChatGPT (GPT-5.1 Thinking)
# Data: 2025-11-19
# ---------------------------------------------------------------------------

import os

# Tenta primeiro importar como pacote (caso o projeto seja usado com `python -m ...`).
# Se falhar, faz um fallback ajustando sys.path para rodar o módulo de forma "solta"
# dentro da pasta assets.
try:
    from .fuzzy_module import calcular_macros
    from .fuzzy_module.calcular_vet import calculo_valor_energetico_total
    from .genetic_module.genetic_module import gerar_cardapio
except ImportError:
    # Fallback para quando rodamos scripts diretamente dentro de assets/
    import sys

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta assets
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)

    from fuzzy_module import calcular_macros
    from fuzzy_module.calcular_vet import calculo_valor_energetico_total
    from genetic_module.genetic_module import gerar_cardapio


def _rotular_dieta(objetivo: int, c_perc: float, p_perc: float, g_perc: float):
    """
    Gera um rótulo simples para o plano de dieta com base em:

    - objetivo:
        0 → hipocalórica
        1 → normocalórica
        2 → hipercalórica
    - percentuais de calorias vindas de carboidratos, proteínas e gorduras.

    Retorna:
        (tipo_dieta: str, tags: List[str])
    """
    tipo = {
        0: "hipocalórica",
        1: "normocalórica",
        2: "hipercalórica",
    }.get(objetivo, "normocalórica")

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
    Gera o plano de dieta completo para um usuário, integrando:
      - Lógica Fuzzy (cálculo de metas de macros e VET)
      - Algoritmo Genético (geração de cardápio)
      - Rotulagem de tipo de dieta

    Parâmetro
    ---------
    dados : dict
        Estrutura esperada:
        {
          "objetivo": 0|1|2,                 # 0: hipocalórica, 1: normocalórica, 2: hipercalórica
          "atividade": 0..10,                # nível de atividade física
          "colesterol": 0..300,             # valor de colesterol total aproximado
          "peso": float,                    # peso em kg

          # parâmetros de organização do cardápio
          "n_refeicoes": 5,

          # restrições alimentares
          "restricoes": {"banidos": ["lactose", "glúten", ...]},

          # orçamento máximo diário estimado (opcional)
          "orcamento_max": 30.0,

          # caminho da tabela TACO reduzida / base de alimentos
          # pode ser:
          #   - "data/taco_min.csv"
          #   - "assets/data/taco_min.csv"
          #   - caminho absoluto
          "tabela_csv": "data/taco_min.csv",

          # parâmetros do Algoritmo Genético (opcionais)
          "ag": {"pop": 100, "ger": 120, "elit": 6, "seed": 42}
        }

    Retorno
    -------
    dict
        {
          "resumo": str,                    # texto resumindo o plano
          "alvos": {
              "vet": float,
              "kcal": float,
              "carb_g": float,
              "prot_g": float,
              "fat_g": float,
              "perc": {
                  "carb": float,
                  "prot": float,
                  "gord": float
              }
          },
          "cardapio": [...],               # lista de refeições e itens (saída do AG)
          "metricas": {...},               # métrica de fitness do melhor cardápio
          "historico_otimizacao": [...],   # histórico das últimas gerações do AG
        }
    """
    # ------------------------------------------------------------------
    # 1) Validação mínima e extração dos dados principais
    # ------------------------------------------------------------------
    # Aqui assumimos que o chamador já garantiu que as chaves existem.
    # Se quiser deixar ainda mais robusto, podemos trocar por `dados.get`
    # e levantar ValueError com mensagens explícitas.
    objetivo = int(dados["objetivo"])
    atividade = int(dados["atividade"])
    colesterol = int(dados["colesterol"])
    peso = float(dados["peso"])

    # ------------------------------------------------------------------
    # 2) Lógica Fuzzy → metas de macronutrientes (g) e VET (kcal)
    # ------------------------------------------------------------------
    # calcular_macros: retorna (carb_g, prot_g, fat_g) usando fuzzy
    carb_g, prot_g, fat_g = calcular_macros(
        objetivo,
        atividade,
        colesterol,
        peso,
        debug=False,  # mantém sem logs extras aqui; o debug pode ser ativado em testes
    )
    # calculo_valor_energetico_total: valor energético alvo em kcal
    vet = calculo_valor_energetico_total(objetivo, peso)

    # ------------------------------------------------------------------
    # 3) Cálculo de percentuais (para rótulo) com base nas calorias dos macros
    # ------------------------------------------------------------------
    c_kcal = carb_g * 4
    p_kcal = prot_g * 4
    g_kcal = fat_g * 9
    total_kcal = max(1, c_kcal + p_kcal + g_kcal)  # evita divisão por zero

    c_perc = c_kcal / total_kcal * 100
    p_perc = p_kcal / total_kcal * 100
    g_perc = g_kcal / total_kcal * 100

    # Define tipo de dieta e tags resumidas (alto carbo, alta proteína, etc.)
    tipo, tags = _rotular_dieta(objetivo, c_perc, p_perc, g_perc)

    # ------------------------------------------------------------------
    # 4) Resolver caminho da tabela CSV (TACO reduzida) de forma robusta
    # ------------------------------------------------------------------
    base_assets = os.path.dirname(os.path.abspath(__file__))  # pasta `assets`
    tabela_csv_raw = dados.get("tabela_csv", "data/taco_min.csv")

    # Se já for caminho absoluto, usa diretamente.
    if os.path.isabs(tabela_csv_raw):
        tabela_csv = tabela_csv_raw
    else:
        # Se vier algo como "assets/data/taco_min.csv" (com ou sem barra invertida),
        # removemos o prefixo "assets/" ou "assets\\" para evitar duplicar a pasta.
        if tabela_csv_raw.startswith("assets/"):
            tabela_csv_raw = tabela_csv_raw[len("assets/") :]
        elif tabela_csv_raw.startswith("assets\\"):
            tabela_csv_raw = tabela_csv_raw[len("assets\\") :]

        # Junta com a pasta assets (onde está este core_engine.py)
        tabela_csv = os.path.join(base_assets, tabela_csv_raw)

    # ------------------------------------------------------------------
    # 5) Montar targets e parâmetros para o Algoritmo Genético
    # ------------------------------------------------------------------
    targets = {
        "kcal": vet,
        "carb_g": carb_g,
        "prot_g": prot_g,
        "fat_g": fat_g,
    }

    params = {
        # parâmetros de layout do cardápio
        "n_refeicoes": int(dados.get("n_refeicoes", 5)),
        "restricoes": dados.get("restricoes", {}),
        "orcamento_max": float(dados.get("orcamento_max", 9999)),

        # caminho para a base de alimentos
        "tabela_csv": tabela_csv,

        # parâmetros do AG (pop, ger, elit, seed, pesos, etc.)
        # são combinados via desempacotamento para permitir override parcial
        **dados.get("ag", {}),
    }

    # ------------------------------------------------------------------
    # 6) Execução do Algoritmo Genético para gerar o cardápio final
    # ------------------------------------------------------------------
    sol = gerar_cardapio(targets, params)

    # ------------------------------------------------------------------
    # 7) Construir um resumo textual amigável para mostrar ao usuário
    # ------------------------------------------------------------------
    resumo = (
        f"Plano {tipo}, "
        + (", ".join(tags) + ", " if tags else "")
        + f"para {peso:.1f} kg: ~{vet:.0f} kcal/dia. Metas: "
        f"CHO {carb_g} g, PRO {prot_g} g, GORD {fat_g} g."
    )

    # ------------------------------------------------------------------
    # 8) Retornar estrutura consolidada
    # ------------------------------------------------------------------
    return {
        "resumo": resumo,
        "alvos": {
            "vet": vet,
            **targets,
            "perc": {
                "carb": c_perc,
                "prot": p_perc,
                "gord": g_perc,
            },
        },
        "cardapio": sol["refeicoes"],
        "metricas": sol["fitness"],
        "historico_otimizacao": sol["historico"],
    }
