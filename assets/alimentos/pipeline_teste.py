"""
pipeline_teste.py
-----------------
Script de teste integrado do NutriBotIA.
"""

import os
import sys
import pandas as pd

# === Garante que a pasta 'alimentos' esteja no sys.path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../assets/alimentos
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Agora o Python enxerga o pacote fuzzy_module e o genetic_module
from fuzzy_module.calcular_prioridade import calcular_prioridade
from genetic_module import gerar_cardapio

# =============================
# 1. Mapeamento texto -> escala 0–10 para o Fuzzy
# =============================

def mapear_renda_fuzzy(renda_str: str) -> float:
    """
    Converte renda em valor aproximado para o universo fuzzy (0 a 10).
    """
    renda_str = (renda_str or "").lower()
    if "baixa" in renda_str:
        return 2.0   # mais perto de "baixa"
    elif "alta" in renda_str:
        return 8.0   # mais perto de "alta"
    else:  # media
        return 5.0


def mapear_tempo_fuzzy(tempo_str: str) -> float:
    """
    Converte tempo em valor aproximado (0 a 10).
    """
    tempo_str = (tempo_str or "").lower()
    if "pouco" in tempo_str:
        return 2.0
    elif "muito" in tempo_str:
        return 8.0
    else:  # medio
        return 5.0


def mapear_saude_fuzzy(saude_str: str) -> float:
    """
    Converte saúde em valor aproximado (0 a 10).
    """
    saude_str = (saude_str or "").lower()
    if "delicada" in saude_str:
        return 2.0
    elif "boa" in saude_str:
        return 8.0
    else:  # ok
        return 5.0


# =============================
# 2. Definição de Cenários de Teste
# =============================

CENARIOS = [
    {
        "nome": "Usuário 1 - Baixa renda, pouco tempo, saúde delicada",
        "renda_str": "baixa",
        "tempo_str": "pouco",
        "saude_str": "delicada",
        "meta_kcal": 1800,
        "restricoes_banidas": ["lactose"],
    },
    {
        "nome": "Usuário 2 - Renda média, tempo médio, saúde ok",
        "renda_str": "media",
        "tempo_str": "medio",
        "saude_str": "ok",
        "meta_kcal": 2200,
        "restricoes_banidas": [],
    },
    {
        "nome": "Usuário 3 - Renda alta, muito tempo, saúde boa",
        "renda_str": "alta",
        "tempo_str": "muito",
        "saude_str": "boa",
        "meta_kcal": 2000,
        "restricoes_banidas": ["gluten"],
    },
]


# =============================
# 3. Função que roda um cenário
# =============================

def rodar_cenario(cenario: dict):
    """
    Executa o fluxo Fuzzy + GA para um cenário de usuário.
    """

    print("\n" + "=" * 70)
    print(f"🔎 CENÁRIO: {cenario['nome']}")
    print("=" * 70)

    renda_str = cenario["renda_str"]
    tempo_str = cenario["tempo_str"]
    saude_str = cenario["saude_str"]
    meta_kcal = cenario["meta_kcal"]
    restricoes_banidas = cenario["restricoes_banidas"]

    # ---------- PRINT 1: Dados de entrada do usuário ----------
    print("\n[INPUT USUÁRIO]")
    print(f"  Renda:        {renda_str}")
    print(f"  Tempo cozinha:{tempo_str}")
    print(f"  Saúde geral:  {saude_str}")
    print(f"  Meta calórica:{meta_kcal} kcal")
    print(f"  Restrições:   {restricoes_banidas if restricoes_banidas else 'nenhuma'}")

    # 1) Mapear para escala 0–10 (Fuzzy)
    renda_val = mapear_renda_fuzzy(renda_str)
    tempo_val = mapear_tempo_fuzzy(tempo_str)
    saude_val = mapear_saude_fuzzy(saude_str)

    # 2) Calcular prioridade fuzzy
    prioridade = calcular_prioridade(renda_val, tempo_val, saude_val)
    prioridade_norm = prioridade / 10.0

    # ---------- PRINT 2: Resultado do Fuzzy ----------
    print("\n[SAÍDA FUZZY]")
    print(f"  Valor fuzzy recebido:")
    print(f"    renda_val       = {renda_val:.1f} (0–10)")
    print(f"    tempo_cozinha   = {tempo_val:.1f} (0–10)")
    print(f"    saude_geral     = {saude_val:.1f} (0–10)")
    print(f"  Prioridade nutr.  = {prioridade:.2f} / 10.00")
    print(f"  Prioridade norm.  = {prioridade_norm:.2f} (0–1)")

    # 3) Ajustar número de gerações do AG com base na prioridade
    n_geracoes = int(20 + 20 * prioridade_norm)  # de 20 a 40
    print("\n[PARÂMETROS DO AG]")
    print(f"  n_geracoes escolhido = {n_geracoes} (20 a 40)")

    # 4) Chamar o Algoritmo Genético
    cardapio_df, individuo, fitness = gerar_cardapio(
        meta_kcal=meta_kcal,
        renda=renda_str,
        restricoes_banidas=restricoes_banidas,
        n_geracoes=n_geracoes,
    )

    # 5) Calcular kcal e custo totais do cardápio
    kcal_total = cardapio_df["kcal"].sum()
    custo_total = cardapio_df["custo_por_porcao"].sum()

    # ---------- PRINT 3: Resultado do AG ----------
    print("\n[SAÍDA DO ALGORITMO GENÉTICO]")
    print(f"  Fitness (penalidade total) = {fitness[0]:.4f}")
    print(f"  Kcal total do cardápio     = {kcal_total:.2f} kcal")
    print(f"  Custo total estimado       = R$ {custo_total:.2f}")

    print("\n[Cardápio sugerido]")
    # Seleciona colunas mais importantes pra visualizar
    colunas_exibir = [c for c in ["nome", "kcal", "custo_por_porcao", "restricao"] if c in cardapio_df.columns]
    print(cardapio_df[colunas_exibir].to_string(index=False))


# =============================
# 4. Main - Executa todos os cenários de teste
# =============================

if __name__ == "__main__":
    print("=== PIPELINE DE TESTE NUTRIBOTIA (Fuzzy + Algoritmo Genético) ===")

    for c in CENARIOS:
        rodar_cenario(c)

    print("\n🧪 Testes finalizados.")
