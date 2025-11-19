# app.py
"""
Aplicação de Teste Rápido — NutriBot IA
---------------------------------------

Este arquivo serve como um *sandbox* para testar rapidamente o motor central
do projeto (`core_engine`), que integra:

- Lógica Fuzzy → cálculo de metas de carboidratos, proteínas e gorduras
- Algoritmo Genético → geração de cardápio otimizado
- Organização e resumo do plano alimentar

Útil para desenvolvimento, debug e validação antes de integrar com API, Chatbot
ou WhatsApp.

Comentários revisados e organizados com auxílio do ChatGPT (GPT-5.1 Thinking)
Data: 2025-11-19
"""

# ---------------------------------------------------------------------------
# Import do módulo principal (core_engine)
# ---------------------------------------------------------------------------
from assets.core_engine import gerar_plano_para_usuario

# ---------------------------------------------------------------------------
# Dados de teste (simulam o fluxo completo do chatbot)
# ---------------------------------------------------------------------------
dados = {
    # Objetivo do usuário:
    #   0 = cutting (emagrecimento)
    #   1 = manutenção
    #   2 = bulking (ganho de massa)
    "objetivo": 2,

    # Nível de atividade física (0 a 10)
    "atividade": 7,

    # Colesterol total estimado (mg/dL)
    "colesterol": 20,

    # Peso corporal (kg)
    "peso": 77.7,

    # Organização do plano
    "n_refeicoes": 5,

    # Restrições alimentares (banir alimentos por nome ou tag)
    "restricoes": {"banidos": ["lactose"]},

    # Limite aproximado de custo para o AG
    "orcamento_max": 30.0,

    # Caminho da base TACO reduzida
    "tabela_csv": "assets/data/taco_min.csv",

    # Parâmetros customizados do Algoritmo Genético
    "ag": {
        # Pesos de erro → (kcal, carbo, prot, gord, custo)
        "pesos": (4.0, 2.5, 1.2, 1.0, 1.0),

        # Limiares de densidade calórica
        "high_density_kcal_threshold": 450,
        "density_penalty_factor": 14.0,
        "dense_big_portion_g": 80,

        # Semente para aleatoriedade
        "low_kcal_bias": 0.6,
        "debug": False,

        # Regras de mínimo por refeição
        "meal_carb_min": 45.0,
        "meal_carb_coeff": 16.0,
    },
}

# ---------------------------------------------------------------------------
# Execução do core_engine → gera o plano completo
# ---------------------------------------------------------------------------
resultado = gerar_plano_para_usuario(dados)

# ---------------------------------------------------------------------------
# Impressão organizada do resultado
# ---------------------------------------------------------------------------

print("\n===== RESUMO DO PLANO =====")
print(resultado["resumo"])

print("\n===== MÉTRICAS FINAIS =====")
print(resultado["metricas"])

print("\n===== CARDÁPIO =====")
for i, refeicao in enumerate(resultado["cardapio"], 1):
    print(f"\nRefeição {i}:")
    for item in refeicao:
        print(f" - {item['nome']} — {item['porcao_g']} g")

print("\n===== FIM DO TESTE =====\n")
