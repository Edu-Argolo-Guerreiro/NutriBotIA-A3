"""
Script: prepara_dados.py
Descrição: Processa a Tabela TACO (taco.xlsx ou taco.csv) e gera a base 'alimentos.csv'
para uso no projeto NutriBotIA.

- Detecta colunas pelo conteúdo do nome (energia, proteína, carboidrato, lipídeo).
- Limpa linha de unidades.
- Converte strings com vírgula para número.
- Gera categorias simples, custo estimado e restrições.
"""

import pandas as pd
import random
import os

if os.path.exists("taco.xlsx"):
    df = pd.read_excel("taco.xlsx")
    print("Lendo taco.xlsx")
elif os.path.exists("taco.csv"):
    df = pd.read_csv("taco.csv", sep=";", encoding="latin1")
    print("Lendo taco.csv")
else:
    raise FileNotFoundError("Nenhum taco.xlsx ou taco.csv encontrado na pasta.")

print("Dimensões originais:", df.shape)
print("Colunas encontradas:", list(df.columns))

col_nome = None
col_kcal = None
col_prot = None
col_carb = None
col_gord = None

for col in df.columns:
    col_lower = str(col).lower()
    if "descri" in col_lower and "alimento" in col_lower:
        col_nome = col
    elif "energia" in col_lower:
        col_kcal = col
    elif "prote" in col_lower:
        col_prot = col
    elif "carbo" in col_lower and "fibra" not in col_lower:
        col_carb = col
    elif "lip" in col_lower:  # lipídeos
        col_gord = col

print("\nMapeamento automático de colunas:")
print("nome      ->", col_nome)
print("kcal      ->", col_kcal)
print("proteína  ->", col_prot)
print("carbo     ->", col_carb)
print("gordura   ->", col_gord)


if None in [col_nome, col_kcal, col_prot, col_carb, col_gord]:
    raise ValueError("Não foi possível identificar todas as colunas necessárias. "
                     "Verifique os nomes no arquivo TACO.")


df = df[[col_nome, col_kcal, col_prot, col_carb, col_gord]].copy()
df.columns = ["nome", "kcal", "proteina", "carbo", "gordura"]


df["nome"] = df["nome"].astype(str)
df = df[~df["nome"].isna()]
df = df[df["nome"].str.strip().ne("")]


for col in ["kcal", "proteina", "carbo", "gordura"]:
 
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace("Tr", "0", regex=False)
        .str.replace("tr", "0", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")


df = df.dropna(subset=["kcal"])


df["nome"] = df["nome"].str.strip()
df = df.drop_duplicates(subset="nome")


def categorizar(nome):
    n = nome.lower()
    if "arroz" in n or "macarr" in n or "pão" in n or "pao" in n or "massa" in n:
        return "carboidrato"
    elif "carne" in n or "frango" in n or "peixe" in n or "ovo" in n:
        return "proteina"
    elif "leite" in n or "queijo" in n or "iogurte" in n:
        return "laticinio"
    elif "banana" in n or "maçã" in n or "maca" in n or "laranja" in n or "maça" in n:
        return "fruta"
    elif "alface" in n or "tomate" in n or "cenoura" in n or "verdura" in n or "legume" in n:
        return "vegetal"
    else:
        return "outros"

df["categoria"] = df["nome"].apply(categorizar)


df["custo_por_porcao"] = [round(random.uniform(0.5, 5.0), 2) for _ in range(len(df))]


def restricao(nome):
    n = nome.lower()
    if "leite" in n or "queijo" in n or "iogurte" in n:
        return "lactose"
    elif "trigo" in n or "pão" in n or "pao" in n or "farinha" in n:
        return "gluten"
    elif "carne" in n or "frango" in n or "peixe" in n or "presunto" in n:
        return "animal"
    else:
        return "nenhuma"

df["restricao"] = df["nome"].apply(restricao)


df.to_csv("alimentos.csv", index=False, encoding="utf-8")

print("\n[OK] Base 'alimentos.csv' gerada com sucesso!")
print("Total de alimentos:", len(df))
print(df.head(10))
