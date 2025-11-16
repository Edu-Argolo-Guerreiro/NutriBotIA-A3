from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import csv, random, math

@dataclass
class FoodItem:
    id: str
    nome: str
    kcal_100g: float
    carb_100g: float
    prot_100g: float
    gord_100g: float
    preco_100g: float = 0.0
    tags: Tuple[str, ...] = ()

def carregar_tabela_alimentos(caminho_csv: str) -> List[FoodItem]:
    itens = []
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                itens.append(FoodItem(
                    id=str(r.get("id") or r.get("ID") or r.get("codigo") or len(itens)+1),
                    nome=r.get("nome") or r.get("alimento") or "item",
                    kcal_100g=float(r.get("kcal_100g") or r.get("kcal") or r.get("energia_kcal") or 0),
                    carb_100g=float(r.get("carb_100g") or r.get("carboidrato_g") or 0),
                    prot_100g=float(r.get("prot_100g") or r.get("proteina_g") or 0),
                    gord_100g=float(r.get("gord_100g") or r.get("lipidio_g") or 0),
                    preco_100g=float(r.get("preco_100g") or 0),
                    tags=tuple((r.get("tags") or "").split("|")) if r.get("tags") else ()
                ))
            except Exception:
                continue
    return [it for it in itens if it.kcal_100g > 0]

def _nutr_por_porcao(item: FoodItem, gramas: float):
    fator = gramas / 100.0
    return (
        item.kcal_100g * fator,
        item.carb_100g * fator,
        item.prot_100g * fator,
        item.gord_100g * fator,
        item.preco_100g * fator,
    )

def _violacao_restricoes(item: FoodItem, restricoes: Dict) -> bool:
    banidos = set(map(str.lower, restricoes.get("banidos", [])))
    if not banidos: 
        return False
    nome = item.nome.lower()
    tags = {t.lower() for t in item.tags}
    return any(b in nome for b in banidos) or (banidos & tags)

def _avalia_cardapio(cardapio, itens_idx, itens, targets, params):
    # Agrega totais
    kcal=carb=prot=gord=custo=0.0
    penal_restr = 0.0
    for refeicao in cardapio:
        for (idx, porcao) in refeicao:
            item = itens[itens_idx[idx]]
            k,c,p,g,pr = _nutr_por_porcao(item, porcao)
            kcal+=k; carb+=c; prot+=p; gord+=g; custo+=pr
            if _violacao_restricoes(item, params.get("restricoes", {})):
                penal_restr += 500.0  # penaliza forte

    # Penalidade por colesterol opcional (se vier dos dados)
    # Aqui como placeholder (não somamos colesterol real por falta de dado)
    # max_colesterol = params.get("restricoes", {}).get("max_colesterol_mg")
    # if max_colesterol and colesterol_total > max_colesterol: penal += ...

    # Erro relativo suave (absoluto) com pesos
    α,β,γ,δ,ε = params.get("pesos", (1.0, 0.7, 0.9, 0.7, 1.0))
    err = (
        α * abs(kcal - targets["kcal"]) +
        β * abs(carb - targets["carb_g"]) * 4 +   # converte macros para kcal-like
        γ * abs(prot - targets["prot_g"]) * 4 +
        δ * abs(gord - targets["fat_g"])  * 9
    )
    excesso_custo = max(0.0, custo - params.get("orcamento_max", float("inf")))
    J = err + ε * excesso_custo + penal_restr
    return J, kcal, carb, prot, gord, custo

def _criar_individuo(n_refeicoes, itens, itens_idx, min_itens=2, max_itens=4):
    # Cada refeição recebe 2–4 itens, porções entre 30g e 200g
    individuo = []
    for _ in range(n_refeicoes):
        n = random.randint(min_itens, max_itens)
        genes = []
        for __ in range(n):
            idx = random.randrange(len(itens_idx))
            porcao = random.choice([40, 60, 80, 100, 120, 150, 200])
            genes.append((idx, porcao))
        individuo.append(genes)
    return individuo

def _mutar(ind, taxa_item=0.2, taxa_porc=0.3, itens_idx=None):
    for refeicao in ind:
        # Troca item
        if random.random() < taxa_item and itens_idx:
            i = random.randrange(len(refeicao))
            refeicao[i] = (random.randrange(len(itens_idx)), refeicao[i][1])
        # Ajusta porção
        if random.random() < taxa_porc:
            j = random.randrange(len(refeicao))
            delta = random.choice([-40, -20, +20, +40])
            nova = max(20, min(300, refeicao[j][1] + delta))
            refeicao[j] = (refeicao[j][0], nova)
    return ind

def _crossover(p1, p2):
    # 1 ponto ao nível de refeição
    n = len(p1)
    if n < 2: return p1[:], p2[:]
    cp = random.randrange(1, n)
    f1 = p1[:cp] + p2[cp:]
    f2 = p2[:cp] + p1[cp:]
    return f1, f2

def gerar_cardapio(targets: Dict, params: Dict) -> Dict:
    """
    targets = {"kcal": int, "carb_g": int, "prot_g": int, "fat_g": int}
    params = {
      "n_refeicoes": 5,
      "restricoes": {"banidos": ["lactose"], "max_colesterol_mg": 300},
      "orcamento_max": 30.0,
      "tabela_csv": "data/taco_min.csv",
      "pop": 80, "ger": 80, "elit": 4,
      "pesos": (1.0,0.7,0.9,0.7,1.0)
    }
    """
    random.seed(params.get("seed", 42))
    n_refeicoes = int(params.get("n_refeicoes", 5))
    pop_size = int(params.get("pop", 80))
    ger = int(params.get("ger", 80))
    elit = int(params.get("elit", 4))

    itens = carregar_tabela_alimentos(params["tabela_csv"])
    if not itens:
        raise RuntimeError("Tabela de alimentos vazia ou inválida.")
    itens_idx = list(range(len(itens)))

    # População
    pop = [_criar_individuo(n_refeicoes, itens, itens_idx) for _ in range(pop_size)]

    def avaliar(ind):
        return _avalia_cardapio(ind, itens_idx, itens, targets, params)

    # Evolução
    historico = []
    for g in range(ger):
        # Avaliação e elitismo
        avals = [(ind, *avaliar(ind)) for ind in pop]
        avals.sort(key=lambda x: x[1])  # por J
        elite = [a[0] for a in avals[:elit]]
        historico.append({
            "ger": g, "best_J": avals[0][1],
            "kcal": avals[0][2], "carb": avals[0][3], "prot": avals[0][4], "gord": avals[0][5], "custo": avals[0][6]
        })

        # Seleção por torneio
        def torneio(k=3):
            cand = random.sample(avals, k)
            cand.sort(key=lambda x: x[1])
            return cand[0][0]

        filhos = elite[:]  # mantém elite
        while len(filhos) < pop_size:
            p1, p2 = torneio(), torneio()
            f1, f2 = _crossover(p1, p2)
            f1 = _mutar(f1, itens_idx=itens_idx)
            f2 = _mutar(f2, itens_idx=itens_idx)
            filhos.extend([f1, f2])
        pop = filhos[:pop_size]

    # Melhor solução final
    final = [(ind, *avaliar(ind)) for ind in pop]
    final.sort(key=lambda x: x[1])
    best, J, kcal, carb, prot, gord, custo = final[0]

    # Organiza por refeição (nome + porção)
    refeicoes = []
    for r in best:
        blocos = []
        for (idx, porcao) in r:
            it = itens[itens_idx[idx]]
            blocos.append({
                "id": it.id, "nome": it.nome, "porcao_g": porcao
            })
        refeicoes.append(blocos)

    return {
        "fitness": {"J": J, "kcal": kcal, "carb_g": carb, "prot_g": prot, "fat_g": gord, "custo": custo},
        "refeicoes": refeicoes,
        "historico": historico[-10:],  # últimas 10 gerações para debug/plot
    }
