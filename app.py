# app.py
from assets.core_engine import gerar_plano_para_usuario

dados = {
    "objetivo": 2,           # 0=cutting, 1=manutenção, 2=bulking
    "atividade": 7,          # 0..10
    "colesterol": 20,
    "peso": 77.7,

    "n_refeicoes": 5,
    "restricoes": {"banidos": ["lactose"]},
    "orcamento_max": 30.0,

    # coloque o caminho certo do seu CSV da TACO
    "tabela_csv": "assets/data/taco_min.csv",

    "ag": {"pop": 80, "ger": 80, "elit": 4, "seed": 7}
}

resultado = gerar_plano_para_usuario(dados)

print("\n===== RESUMO DO PLANO =====")
print(resultado["resumo"])

print("\n===== MÉTRICAS FINAIS =====")
print(resultado["metricas"])

print("\n===== CARDÁPIO =====")
for i, refeicao in enumerate(resultado["cardapio"], 1):
    print(f"\nRefeição {i}:")
    for item in refeicao:
        print(f" - {item['nome']} — {item['porcao_g']} g")
