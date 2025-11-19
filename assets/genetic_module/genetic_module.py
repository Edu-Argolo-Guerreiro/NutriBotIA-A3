# assets/genetic_module/genetic_module.py
"""
Módulo: genetic_module
----------------------

Responsável por gerar um cardápio diário utilizando um
Algoritmo Genético (AG), a partir de:

- Metas nutricionais alvo (kcal, carboidratos, proteínas, gorduras)
- Tabela de alimentos (TACO reduzida, por exemplo)
- Restrições (ex.: alimentos banidos, orçamento máximo, etc.)

O AG trabalha criando indivíduos onde cada indivíduo representa
um dia de cardápio, estruturado em N refeições.
Cada refeição tem de 2 a 3 itens, com:
    - 1 fonte base de carboidrato
    - 1 fonte principal de proteína
    - 0 ou 1 item “extra” (fruta, legume, cereal etc.)

A função principal exposta é:

    gerar_cardapio(targets: Dict, params: Dict) -> Dict
"""

# ---------------------------------------------------------------------------
# Comentários e ajustes de revisão inseridos com auxílio do ChatGPT (GPT-5.1 Thinking)
# Data: 2025-11-19
# ---------------------------------------------------------------------------

from dataclasses import dataclass
from typing import List, Dict, Tuple
import csv
import random

# Mantido comentado para evitar poluir o log ao importar o módulo como biblioteca.
# Descomente se precisar depurar problemas de import.
# print(">>> genetic_module carregado de:", __file__)  # opcional, útil para debug de import


# ============================================================
#   Estrutura de dados dos alimentos + carregamento da tabela
# ============================================================
@dataclass
class FoodItem:
    """
    Representa um alimento da tabela, padronizado em por 100 g.
    """
    id: str
    nome: str
    kcal_100g: float
    carb_100g: float
    prot_100g: float
    gord_100g: float
    preco_100g: float = 0.0
    tags: Tuple[str, ...] = ()


def carregar_tabela_alimentos(caminho_csv: str) -> List[FoodItem]:
    """
    Lê um CSV de alimentos e devolve uma lista de FoodItem.

    Espera colunas compatíveis com:
      - id / ID / codigo
      - nome / alimento
      - kcal_100g / kcal / energia_kcal
      - carb_100g / carboidrato_g
      - prot_100g / proteina_g
      - gord_100g / lipidio_g
      - preco_100g (opcional)
      - tags (opcional, separadas por '|')

    Linhas com dados numéricos inválidos são ignoradas.
    """
    itens: List[FoodItem] = []

    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                it = FoodItem(
                    id=str(r.get("id") or r.get("ID") or r.get("codigo") or len(itens) + 1),
                    nome=r.get("nome") or r.get("alimento") or "item",
                    kcal_100g=float(r.get("kcal_100g") or r.get("kcal") or r.get("energia_kcal") or 0),
                    carb_100g=float(r.get("carb_100g") or r.get("carboidrato_g") or 0),
                    prot_100g=float(r.get("prot_100g") or r.get("proteina_g") or 0),
                    gord_100g=float(r.get("gord_100g") or r.get("lipidio_g") or 0),
                    preco_100g=float(r.get("preco_100g") or 0),
                    tags=tuple((r.get("tags") or "").split("|")) if r.get("tags") else (),
                )
                # precisa ter energia > 0 e pelo menos um macro não-zero
                if it.kcal_100g > 0 and (it.carb_100g > 0 or it.prot_100g > 0 or it.gord_100g > 0):
                    itens.append(it)
            except Exception:
                # se ocorrer erro em alguma linha, apenas ignora
                # (mantém robustez caso a base esteja "suja")
                continue

    return itens


# ============================================================
#                       Funções auxiliares
# ============================================================
def _has_tag(item: FoodItem, tag: str) -> bool:
    """Retorna True se o alimento possuir a *tag* (case-insensitive)."""
    return any(t.lower() == tag.lower() for t in item.tags)


def _nome_match(item: FoodItem, frag: str) -> bool:
    """
    Verifica se um fragmento de texto aparece no nome do alimento
    (case-insensitive).
    """
    return frag.lower() in (item.nome or "").lower()


def _is_carb_base(item: FoodItem) -> bool:
    """
    Define se o alimento pode ser considerado como base de carboidrato.

    Critérios:
      - carboidrato por 100 g >= 12 g (evita legumes/folhas com pouco CHO)
      - carboidrato é o macro dominante (>= proteína e >= gordura)
    """
    if item.carb_100g < 12:
        return False
    return item.carb_100g >= max(item.prot_100g, item.gord_100g)


def _is_high_protein(item: FoodItem) -> bool:
    """
    Considera um alimento como 'proteico' se possui >= 15 g de proteína / 100 g.
    Ex.: frango, ovos, iogurte proteico, whey etc.
    """
    return item.prot_100g >= 15.0


def _is_high_fat(item: FoodItem) -> bool:
    """
    Marca alimentos gordurosos, ideal para limitar porção:
    - >= 15 g de gordura / 100 g
    - OU tags de gordura/oleaginosa/semente
    """
    if item.gord_100g >= 15:
        return True
    if _has_tag(item, "gordura") or _has_tag(item, "oleaginosa") or _has_tag(item, "semente"):
        return True
    return False


def _safe_portion(item: FoodItem, por: int) -> int:
    """
    Garante porções em uma faixa realista e segura.

    Regras:
      - limite global: 20 a 250 g
      - se muito denso (> 500 kcal/100g), limita a 120 g
      - se muito proteico, limita a 180 g
      - se muito gorduroso, limita a 60 g
      - alguns ajustes “soft” por nome (whey, abacate, pasta de amendoim etc.)
    """
    # Limite bruto
    por = max(20, min(250, por))

    # alimentos extremamente densos
    if item.kcal_100g > 500:
        por = min(por, 120)

    # proteínas concentradas
    if _is_high_protein(item):
        por = min(por, 180)

    # gorduras (castanhas, óleos, sementes)
    if _is_high_fat(item):
        por = min(por, 60)

    # limites adicionais por nome, para evitar exageros
    if _nome_match(item, "whey"):
        por = min(por, 60)
    if _nome_match(item, "pasta de amendoim") or _nome_match(item, "amendoim"):
        por = min(por, 40)
    if _nome_match(item, "abacate"):
        por = min(por, 120)

    return por


def _nutr_por_porcao(item: FoodItem, gramas: float) -> Tuple[float, float, float, float, float]:
    """
    Calcula os nutrientes de uma porção específica (em gramas),
    a partir dos valores por 100 g.

    Retorna: (kcal, carboidrato_g, proteina_g, gordura_g, preco)
    """
    fator = gramas / 100.0
    return (
        item.kcal_100g * fator,
        item.carb_100g * fator,
        item.prot_100g * fator,
        item.gord_100g * fator,
        item.preco_100g * fator,
    )


def _violacao_restricoes(item: FoodItem, restricoes: Dict) -> bool:
    """
    Verifica se o alimento viola alguma restrição declarada.

    Atualmente:
      - restricoes["banidos"]: lista de palavras-chave que não podem
        aparecer nem no nome nem nas tags do alimento.
    """
    banidos = set(map(str.lower, restricoes.get("banidos", [])))
    if not banidos:
        return False

    nome = item.nome.lower()
    tags = {t.lower() for t in item.tags}

    # se fragmento banido aparecer no nome ou em alguma tag → violação
    return any(b in nome for b in banidos) or (banidos & tags)


# ============================================================
#                     Função de Fitness
# ============================================================
def _avalia_cardapio(
    cardapio,
    itens_idx: List[int],
    itens: List[FoodItem],
    targets: Dict[str, float],
    params: Dict,
):
    """
    Avalia um indivíduo (cardápio completo do dia).

    Critérios usados:
      - Aproximação das metas globais:
          * kcal
          * carboidratos (g)
          * proteínas (g)
          * gorduras (g)
      - Penaliza:
          * violação de restrições (alimentos banidos)
          * refeições com pouco carboidrato/proteína
          * leve excesso de densidade calórica
          * falta de variedade (muitas gramas do mesmo alimento)
          * excesso exagerado de proteína (acima de ~140% da meta)

    Retorna:
        (J_total, kcal, carb, prot, gord, custo)
    """
    kcal = carb = prot = gord = custo = 0.0
    penal_restr = 0.0
    dens_penalty = 0.0
    meal_penalty = 0.0
    variety_penalty = 0.0

    # quanto de cada alimento é usado ao longo do dia
    uso_por_id: Dict[str, float] = {}

    # parâmetros por refeição (para bulking mais realista)
    meal_min_carb = float(params.get("meal_carb_min", 45.0))      # g CHO / refeição
    meal_carb_weight = float(params.get("meal_carb_weight", 14.0))
    meal_min_prot = float(params.get("meal_prot_min", 15.0))      # g PRO / refeição
    meal_prot_weight = float(params.get("meal_prot_weight", 10.0))

    # limiar de densidade calórica (kcal/100g) acima do qual começamos a penalizar
    dens_thr = float(params.get("high_density_kcal_threshold", 550.0))

    restricoes = params.get("restricoes", {})

    # --- loop por refeição ---
    for refeicao in cardapio:
        carbs_ref = 0.0
        prot_ref = 0.0

        for (idx, porcao) in refeicao:
            item = itens[itens_idx[idx]]
            porcao = _safe_portion(item, porcao)

            k, c, p, g, pr = _nutr_por_porcao(item, porcao)
            kcal += k
            carb += c
            prot += p
            gord += g
            custo += pr

            carbs_ref += c
            prot_ref += p

            uso_por_id[item.id] = uso_por_id.get(item.id, 0.0) + porcao

            # densidade muito alta → leve penalidade
            if item.kcal_100g > dens_thr:
                dens_penalty += (item.kcal_100g - dens_thr) * (porcao / 100.0) * 0.2

            # viola alimento banido
            if _violacao_restricoes(item, restricoes):
                penal_restr += 500.0

        # mínimo de carbo / refeição
        if carbs_ref < meal_min_carb:
            meal_penalty += (meal_min_carb - carbs_ref) * meal_carb_weight

        # mínimo de proteína / refeição
        if prot_ref < meal_min_prot:
            meal_penalty += (meal_min_prot - prot_ref) * meal_prot_weight

    # penalidade por falta de variedade (muitas gramas do mesmo alimento no dia)
    for _id, gramas in uso_por_id.items():
        if gramas > 350:  # mais de ~3,5 porções do mesmo alimento
            variety_penalty += (gramas - 350) * 2.0

    # --- Metas globais ---
    alvo_kcal = float(targets["kcal"])
    alvo_c = float(targets["carb_g"])
    alvo_p = float(targets["prot_g"])
    alvo_g = float(targets["fat_g"])

    # pesos do erro (podem ser ajustados via params["pesos"])
    # maior peso em kcal e carboidratos; proteína com peso extra no excesso.
    α, β, γ, δ, ε = params.get("pesos", (4.0, 3.2, 1.8, 1.2, 1.0))

    # assimetrias:
    # kcal: ficar ABAIXO dói mais que ACIMA
    if kcal < alvo_kcal:
        kcal_pen = 2.2 * (alvo_kcal - kcal)
    else:
        kcal_pen = 1.0 * (kcal - alvo_kcal)

    # carbo: déficit dói mais que excesso
    if carb < alvo_c:
        carb_pen = 2.0 * (alvo_c - carb) * 4.0
    else:
        carb_pen = 1.0 * (carb - alvo_c) * 4.0

    # proteína: excesso dói mais que déficit
    if prot > alvo_p:
        prot_pen = 2.5 * (prot - alvo_p) * 4.0
    else:
        prot_pen = 1.0 * (alvo_p - prot) * 4.0

    # gordura: assimetria mais suave
    if gord < alvo_g:
        gord_pen = 1.2 * (alvo_g - gord) * 9.0
    else:
        gord_pen = 1.0 * (gord - alvo_g) * 9.0

    # penal extra se proteína estourar MUITO (acima de 140% da meta)
    prot_extra_pen = 0.0
    lim_prot_alto = alvo_p * 1.4
    if prot > lim_prot_alto:
        prot_extra_pen = (prot - lim_prot_alto) * 40.0

    # custo além do orçamento
    excesso_custo = max(0.0, custo - params.get("orcamento_max", float("inf")))

    # erro total ponderado (sem custo / penalidades ainda)
    err = α * kcal_pen + β * carb_pen + γ * prot_pen + δ * gord_pen

    J = (
        err
        + ε * excesso_custo
        + penal_restr
        + dens_penalty
        + meal_penalty
        + variety_penalty
        + prot_extra_pen
    )

    return J, kcal, carb, prot, gord, custo


# ============================================================
#                Operadores do Algoritmo Genético
# ============================================================
def _criar_individuo(
    n_refeicoes: int,
    itens: List[FoodItem],
    itens_idx: List[int],
    min_itens: int = 2,
    max_itens: int = 3,
    low_kcal_bias: float = 0.6,
):
    """
    Cria um indivíduo inicial (cardápio do dia).

    Representação:
        cardápio = List[refeição]
        refeição = List[(idx_item, porcao_g)]
        idx_item = índice dentro de `itens_idx` (não diretamente em `itens`)

    Estratégia:
      - Preferir itens menos calóricos (low_kcal_bias)
      - Para cada refeição:
          * 1 alimento base de carbo
          * 1 alimento proteico
          * 0–1 alimento extra neutro
    """
    # Ordena por kcal para começar preferindo itens menos densos.
    # Atenção: os elementos em itens_idx são índices em `itens`.
    idx_sorted = sorted(itens_idx, key=lambda i: itens[i].kcal_100g)
    corte = max(1, int(len(idx_sorted) * float(low_kcal_bias)))
    base_pool = idx_sorted[:corte] if corte < len(idx_sorted) else idx_sorted

    # pools especializados
    carb_pool = [i for i in base_pool if _is_carb_base(itens[i])] or base_pool[:]
    prot_pool = [i for i in base_pool if _is_high_protein(itens[i])] or base_pool[:]
    neutro_pool = [i for i in base_pool if not _is_high_fat(itens[i])] or base_pool[:]

    individuo = []

    for _ in range(n_refeicoes):
        n = random.randint(min_itens, max_itens)
        genes = []

        # 1) sempre 1 carbo base
        idx_carb = random.choice(carb_pool)  # índice em `itens`
        por_carb = _safe_portion(
            itens[idx_carb],
            random.choice([120, 150, 180, 200]),
        )
        # converte para índice no vetor `itens_idx`
        genes.append((itens_idx.index(idx_carb), por_carb))

        # 2) sempre 1 proteico
        idx_prot = random.choice(prot_pool)
        por_prot = _safe_portion(
            itens[idx_prot],
            random.choice([70, 90, 110, 130]),
        )
        genes.append((itens_idx.index(idx_prot), por_prot))

        # 3) opcional: 1 extra neutro (legume, fruta, cereal, etc.)
        if n > 2:
            idx_extra = random.choice(neutro_pool)
            por_extra = _safe_portion(
                itens[idx_extra],
                random.choice([60, 80, 100]),
            )
            genes.append((itens_idx.index(idx_extra), por_extra))

        individuo.append(genes)

    return individuo


def _mutar(
    ind,
    taxa_item: float = 0.25,
    taxa_porc: float = 0.40,
    itens_idx: List[int] | None = None,
    contexto: Dict | None = None,
):
    """
    Operador de mutação:
      - troca itens (com probabilidade taxa_item)
      - ajusta porções (com probabilidade taxa_porc)
      - garante que cada refeição tenha:
          * pelo menos 1 proteico
          * pelo menos 1 base de carbo

    `itens_idx` e `contexto` são usados para mapear os índices internos
    do indivíduo para a lista original de alimentos.
    """
    itens = contexto.get("itens") if contexto else None
    full_idx = contexto.get("itens_idx") if contexto else itens_idx

    for refeicao in ind:
        # troca item (altera o índice do gene mantendo porção)
        if random.random() < taxa_item and itens_idx:
            i = random.randrange(len(refeicao))
            refeicao[i] = (random.randrange(len(itens_idx)), refeicao[i][1])

        # ajusta porção
        if random.random() < taxa_porc and len(refeicao) > 0:
            j = random.randrange(len(refeicao))
            delta = random.choice([-20, +20])
            idxj, porj = refeicao[j]
            if itens is not None and full_idx is not None:
                itemj = itens[full_idx[idxj]]
                nova = _safe_portion(itemj, porj + delta)
            else:
                # fallback genérico se contexto não estiver preenchido
                nova = max(20, min(200, porj + delta))
            refeicao[j] = (idxj, nova)

        # garante sempre proteína + carbo em cada refeição
        if itens is not None and full_idx is not None and len(refeicao) > 0:
            has_prot = any(_is_high_protein(itens[full_idx[idx]]) for (idx, _) in refeicao)
            has_carb = any(_is_carb_base(itens[full_idx[idx]]) for (idx, _) in refeicao)

            # se não tiver proteína, substitui um gene por alimento proteico
            if not has_prot:
                j = random.randrange(len(refeicao))
                prot_ids = [i for i in full_idx if _is_high_protein(itens[i])] or full_idx
                idx_p = random.choice(prot_ids)
                por = refeicao[j][1]
                por = _safe_portion(itens[idx_p], por)
                refeicao[j] = (full_idx.index(idx_p), por)

            # se não tiver carbo base, substitui um gene por base de carbo
            if not has_carb:
                j = random.randrange(len(refeicao))
                carb_ids = [i for i in full_idx if _is_carb_base(itens[i])] or full_idx
                idx_c = random.choice(carb_ids)
                por = refeicao[j][1]
                por = _safe_portion(itens[idx_c], por)
                refeicao[j] = (full_idx.index(idx_c), por)

    return ind


def _crossover(p1, p2):
    """
    Crossover de 1 ponto ao nível de refeição.

    p1, p2: indivíduos (listas de refeições)
    """
    n = len(p1)
    if n < 2:
        # com menos de 2 refeições não há ponto de corte válido
        return p1[:], p2[:]
    cp = random.randrange(1, n)
    return p1[:cp] + p2[cp:], p2[:cp] + p1[cp:]


# ============================================================
#           Ajuste global de calorias (pós-processamento)
# ============================================================
def _totais_cardapio(sol, itens_idx: List[int], itens: List[FoodItem]):
    """
    Calcula totais de kcal, CHO, PRO, GORD, custo
    para um cardápio completo.
    """
    kcal = carb = prot = gord = custo = 0.0
    for ref in sol:
        for (idx, por) in ref:
            it = itens[itens_idx[idx]]
            k, c, p, g, pr = _nutr_por_porcao(it, por)
            kcal += k
            carb += c
            prot += p
            gord += g
            custo += pr
    return kcal, carb, prot, gord, custo


def _escala_para_kcal(
    sol,
    itens_idx: List[int],
    itens: List[FoodItem],
    targets: Dict[str, float],
    fator_min: float = 0.8,
    fator_max: float = 1.4,
):
    """
    Escala TODAS as porções por um fator global para aproximar
    as calorias em relação ao alvo.

    fator = alvo_kcal / kcal_atual, limitado por [fator_min, fator_max].

    Isso ajuda a:
      - reduzir ou aumentar tudo proporcionalmente
      - sem quebrar o padrão do cardápio encontrado.
    """
    kcal_atual, carb, prot, gord, custo = _totais_cardapio(sol, itens_idx, itens)
    alvo = float(targets["kcal"])
    if kcal_atual <= 0:
        # evita divisão por zero; neste caso não há como escalar
        return sol

    fator = alvo / kcal_atual
    fator = max(fator_min, min(fator_max, fator))

    # se já está bem próximo, não mexe
    if 0.95 <= fator <= 1.05:
        return sol

    nova_sol = []
    for ref in sol:
        nova_ref = []
        for (idx, por) in ref:
            it = itens[itens_idx[idx]]
            novo_por = int(round(por * fator))
            novo_por = _safe_portion(it, novo_por)
            nova_ref.append((idx, novo_por))
        nova_sol.append(nova_ref)

    return nova_sol


# ============================================================
#                 Função principal do módulo
# ============================================================
def gerar_cardapio(targets: Dict[str, float], params: Dict) -> Dict:
    """
    Gera um cardápio otimizado via Algoritmo Genético.

    targets:
        {
          "kcal":   int,
          "carb_g": int,
          "prot_g": int,
          "fat_g":  int
        }

    params (exemplo):
        {
          "n_refeicoes": 5,
          "restricoes": {"banidos": ["lactose"]},
          "orcamento_max": 30.0,
          "tabela_csv": "assets/data/taco_min.csv",

          # parâmetros do AG:
          "pop": 120,
          "ger": 200,
          "elit": 6,
          "seed": 7,

          # pesos de erro:
          "pesos": (4.0, 3.2, 1.8, 1.2, 1.0),

          # outros:
          "high_density_kcal_threshold": 550,
          "low_kcal_bias": 0.6,
          "meal_carb_min": 35.0,
          "meal_prot_min": 18.0
        }

    Retorna:
        {
          "fitness":  { "J": ..., "kcal": ..., "carb_g": ..., "prot_g": ..., "fat_g": ..., "custo": ... },
          "refeicoes": [
              [ {"id":..., "nome":..., "porcao_g":...}, ... ],  # refeição 1
              ...
          ],
          "historico": [... últimas 10 gerações ...]
        }
    """
    # semente de aleatoriedade para reprodutibilidade
    random.seed(params.get("seed", 42))

    # hiperparâmetros do AG
    n_refeicoes = int(params.get("n_refeicoes", 5))
    pop_size = int(params.get("pop", 120))
    ger = int(params.get("ger", 200))
    elit = int(params.get("elit", 6))
    low_bias = float(params.get("low_kcal_bias", 0.6))

    # carrega tabela de alimentos
    tabela_csv = params.get("tabela_csv")
    if not tabela_csv:
        raise ValueError("Parâmetro obrigatório ausente: 'tabela_csv' com o caminho do arquivo de alimentos.")

    itens = carregar_tabela_alimentos(tabela_csv)
    if not itens:
        raise RuntimeError("Tabela de alimentos vazia ou inválida.")
    itens_idx = list(range(len(itens)))

    # população inicial
    pop = [
        _criar_individuo(
            n_refeicoes,
            itens,
            itens_idx,
            min_itens=2,
            max_itens=3,
            low_kcal_bias=low_bias,
        )
        for _ in range(pop_size)
    ]

    def avaliar(ind):
        return _avalia_cardapio(ind, itens_idx, itens, targets, params)

    historico = []

    # loop de gerações
    for g in range(ger):
        # avals: (indivíduo, J, kcal, carb, prot, gord, custo)
        avals = [(ind, *avaliar(ind)) for ind in pop]
        avals.sort(key=lambda x: x[1])  # ordena por J (fitness) crescente
        elite = [a[0] for a in avals[:elit]]

        historico.append(
            {
                "ger": g,
                "best_J": avals[0][1],
                "kcal": avals[0][2],
                "carb": avals[0][3],
                "prot": avals[0][4],
                "gord": avals[0][5],
                "custo": avals[0][6],
            }
        )

        # seleção por torneio
        def torneio(k: int = 3):
            cand = random.sample(avals, k)
            cand.sort(key=lambda x: x[1])
            return cand[0][0]

        filhos = elite[:]
        ctx = {"itens": itens, "itens_idx": itens_idx}
        while len(filhos) < pop_size:
            p1, p2 = torneio(), torneio()
            f1, f2 = _crossover(p1, p2)
            f1 = _mutar(f1, itens_idx=itens_idx, contexto=ctx)
            f2 = _mutar(f2, itens_idx=itens_idx, contexto=ctx)
            filhos.extend([f1, f2])

        # garante tamanho exato da população (caso estoure ao adicionar pares)
        pop = filhos[:pop_size]

    # melhor solução final
    final = [(ind, *avaliar(ind)) for ind in pop]
    final.sort(key=lambda x: x[1])
    best, J, kcal, carb, prot, gord, custo = final[0]

    # ajuste global pra aproximar das kcal alvo
    best = _escala_para_kcal(best, itens_idx, itens, targets, fator_min=0.8, fator_max=1.8)
    J, kcal, carb, prot, gord, custo = _avalia_cardapio(best, itens_idx, itens, targets, params)

    # organiza saída em formato amigável
    refeicoes = []
    for r in best:
        blocos = []
        for (idx, porcao) in r:
            it = itens[itens_idx[idx]]
            porcao = _safe_portion(it, porcao)
            blocos.append(
                {
                    "id": it.id,
                    "nome": it.nome,
                    "porcao_g": porcao,
                }
            )
        refeicoes.append(blocos)

    return {
        "fitness": {
            "J": J,
            "kcal": kcal,
            "carb_g": carb,
            "prot_g": prot,
            "fat_g": gord,
            "custo": custo,
        },
        "refeicoes": refeicoes,
        "historico": historico[-10:],  # últimas 10 gerações (pra plot/relatório)
    }
