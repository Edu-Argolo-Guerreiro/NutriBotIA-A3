# assets/chatbot/chatbot_engine.py

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Any, List
import json
import os
import sys

from openai import OpenAI

# =======================================
#  Import do core_engine (AG + Fuzzy)
# =======================================
# Tentativa 1: import relativo (quando o projeto é usado como pacote)
try:
    from ..core_engine import gerar_plano_para_usuario
except ImportError:
    # Tentativa 2: ajustar sys.path para rodar em modo "script solto"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    from core_engine import gerar_plano_para_usuario


print(">>> chatbot_engine carregado de:", __file__)


# =======================================
#  Estado da conversa
# =======================================
@dataclass
class ChatState:
    etapa: str = "inicio"
    dados: Dict[str, Any] = field(default_factory=dict)
    terminou: bool = False


# =======================================
#  Mensagens fixas
# =======================================
MSG_BOAS_VINDAS = (
    "Olá! Eu sou o NutriBot IA 🤖🥦\n"
    "Vou te ajudar a gerar um plano alimentar personalizado.\n\n"
    "Você pode digitar 'sair' a qualquer momento para encerrar.\n"
    "Vamos começar!\n\n"
    "Qual é o seu *objetivo* principal?\n"
    "- 0 = Emagrecer\n"
    "- 1 = Manter peso\n"
    "- 2 = Ganhar massa (hipercalórica)\n\n"
    "Digite 0, 1 ou 2:"
)


# =======================================
#  Funções de parsing / utilitários
# =======================================
def _interpretar_objetivo(msg: str) -> Optional[int]:
    msg = msg.strip().lower()
    if msg in ("0", "emagrecer", "perder peso", "perda de peso"):
        return 0
    if msg in ("1", "manter", "manutenção", "manter peso", "manutencao"):
        return 1
    if msg in ("2", "ganhar", "ganhar massa", "hipercalorica", "hipercalórica"):
        return 2
    return None


def _parse_float(msg: str) -> Optional[float]:
    try:
        msg = msg.replace(",", ".")
        return float(msg)
    except Exception:
        return None


def _parse_int(msg: str) -> Optional[int]:
    try:
        return int(msg)
    except Exception:
        return None


def _parse_restricoes(msg: str) -> Dict[str, list]:
    """
    Ex.: 'lactose, camarão' -> {"banidos": ["lactose", "camarão"]}.
    Se o usuário escreve 'nenhuma', retorna dict vazio.
    """
    msg = msg.strip().lower()
    if msg in ("nenhuma", "nao", "não", "sem", "sem restricoes", "sem restrições"):
        return {}
    itens = [p.strip() for p in msg.split(",") if p.strip()]
    return {"banidos": itens} if itens else {}


# =======================================
#  Formatadores de saída (AG → texto)
# =======================================
def _formatar_plano_bruto(resultado: Dict) -> str:
    """
    Formato simples, direto do AG, sem intervenção do ChatGPT.
    """
    resumo = resultado["resumo"]
    metricas = resultado["metricas"]
    cardapio = resultado["cardapio"]

    linhas: List[str] = []
    linhas.append("===== RESUMO DO PLANO =====")
    linhas.append(resumo)
    linhas.append("")
    linhas.append("===== MÉTRICAS FINAIS =====")
    linhas.append(str(metricas))
    linhas.append("")
    linhas.append("===== CARDÁPIO =====")
    linhas.append("")

    for i, refeicao in enumerate(cardapio, start=1):
        linhas.append(f"Refeição {i}:")
        for item in refeicao:
            nome = item["nome"]
            por = item["porcao_g"]
            linhas.append(f" - {nome} — {por} g")
        linhas.append("")

    linhas.append("Se quiser, posso te ajudar a gerar outro plano. É só digitar 'novo'.")
    return "\n".join(linhas)


def _cardapio_em_texto(cardapio) -> str:
    """
    Transforma a lista de refeições do AG em texto simples
    para enviar no prompt do ChatGPT.
    """
    linhas: List[str] = []
    for i, refeicao in enumerate(cardapio, start=1):
        linhas.append(f"Refeição {i}:")
        for item in refeicao:
            nome = item["nome"]
            gr = item["porcao_g"]
            linhas.append(f" - {nome} — {gr} g")
        linhas.append("")
    return "\n".join(linhas)


def _cardapio_em_json(cardapio) -> str:
    """
    Se quiser mandar como JSON no prompt.
    (Não é obrigatório, mas deixamos pronto.)
    """
    return json.dumps(cardapio, ensure_ascii=False, indent=2)


# =======================================
#  Integração com OpenAI (ChatGPT)
# =======================================
_openai_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """
    Cria (ou reutiliza) um cliente da OpenAI usando a variável
    de ambiente OPENAI_API_KEY.
    """
    global _openai_client
    if _openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não definida nas variáveis de ambiente.")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def humanizar_plano_com_chatgpt(resumo: str, metricas: Dict, cardapio: list) -> str:
    """
    Usa o modelo da OpenAI como 'nutricionista conversacional':
    - Organiza as refeições em cardápio realista
    - Pode ajustar levemente as porções (±15%) para ficar funcional
    - Sugere receitas / modo de preparo simples
    Retorna um texto pronto para o usuário.
    """
    client = _get_client()

    cardapio_texto = _cardapio_em_texto(cardapio)

    prompt = f"""
Você é um(a) nutricionista esportivo(a) e chef de cozinha.

Um algoritmo de Lógica Fuzzy + Algoritmo Genético gerou um plano alimentar com base
no objetivo, peso, atividade física e colesterol do usuário.

RESUMO DO PLANO-ALVO:
{resumo}

MÉTRICAS NUTRICIONAIS DO PLANO GERADO (valores atuais):
{json.dumps(metricas, ensure_ascii=False, indent=2)}

CARDÁPIO BRUTO GERADO PELO ALGORITMO (lista de alimentos com gramas):
{cardapio_texto}

Sua tarefa:

1. Transformar esse cardápio em um cardápio diário REALISTA e organizado em 3 a 6 refeições, com:
   - Nome da refeição (ex.: Café da manhã, Almoço, Lanche da tarde, Jantar, Ceia)
   - Lista de alimentos por refeição (com quantidades aproximadas em gramas ou unidades)
   - Sugestão de preparo (ex.: "omelete com...", "salada de...", "prato montado com...").

2. Você pode AJUSTAR as porções em até ±15% para deixar o prato mais funcional
   (por exemplo, arredondar 63 g para 60 g, juntar alimentos parecidos, etc.),
   desde que o plano continue COERENTE com o número de calorias e macros do resumo.

3. Evite combinações estranhas (ex.: muita castanha sozinha, vegetais aleatórios sem fonte de carboidrato ou proteína).
   Sempre que possível, monte refeições com:
   - uma fonte de carboidrato principal,
   - uma fonte de proteína principal,
   - vegetais e/ou frutas,
   - gorduras boas em quantidade moderada.

4. Responda APENAS com o cardápio humanizado, em português, no seguinte formato:

===== PLANO ALIMENTAR SUGERIDO =====

Refeição 1 – Nome:
- alimento 1 — quantidade
- alimento 2 — quantidade
Observações / modo de preparo: ...

Refeição 2 – Nome:
...

No final, faça UMA frase breve reforçando que esse plano é uma sugestão gerada por IA
e não substitui acompanhamento com nutricionista.
    """

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",  # ajuste para o modelo que você tiver acesso
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um(a) nutricionista esportivo(a) que monta cardápios "
                    "equilibrados, práticos e em linguagem acessível."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    return resp.choices[0].message.content.strip()


def _formatar_plano_com_ia(resultado: Dict) -> str:
    """
    Tenta humanizar o plano com ChatGPT; se der erro, volta para o formato bruto.
    """
    resumo = resultado["resumo"]
    metricas = resultado["metricas"]
    cardapio = resultado["cardapio"]

    try:
        plano_humano = humanizar_plano_com_chatgpt(resumo, metricas, cardapio)
        texto = (
            "Vou te mostrar o plano de forma organizada e fácil de seguir:\n\n"
            + plano_humano
        )
    except Exception as e:
        # fallback se der erro na API
        print("Erro ao chamar ChatGPT:", e)
        texto = (
            resumo
            + "\n\n"
            "Não consegui humanizar o cardápio com IA agora, então vou te mostrar "
            "o plano bruto gerado pelo algoritmo:\n\n"
            + _cardapio_em_texto(cardapio)
        )

    return texto


# =======================================
#  Função principal do chatbot
# =======================================
def processar_mensagem(state: ChatState, mensagem: str) -> Tuple[str, ChatState]:
    """
    Recebe o estado atual e a mensagem do usuário.
    Retorna (resposta_do_bot, novo_estado).

    Essa função é o "cérebro" do fluxo conversacional.
    Pode ser usada tanto em linha de comando, quanto WhatsApp, Web, etc.
    """
    msg = mensagem.strip()

    # Comando global 'sair'
    if msg.lower() in ("sair", "exit", "quit"):
        state.terminou = True
        return "Tudo bem! Encerrando a conversa. Qualquer coisa é só chamar novamente. 👋", state

    # Recomeçar do zero
    if msg.lower() in ("novo", "recomecar", "recomeçar", "reset"):
        state = ChatState(etapa="inicio", dados={})
        return MSG_BOAS_VINDAS, state

    # ----------------------
    # Fluxo por etapa
    # ----------------------
    if state.etapa == "inicio":
        state.etapa = "objetivo"
        return MSG_BOAS_VINDAS, state

    # 1) Objetivo
    if state.etapa == "objetivo":
        objetivo = _interpretar_objetivo(msg)
        if objetivo is None:
            return (
                "Não entendi o objetivo. Por favor, responda com:\n"
                "0 = Emagrecer | 1 = Manter peso | 2 = Ganhar massa.",
                state,
            )
        state.dados["objetivo"] = objetivo
        state.etapa = "peso"
        return "Perfeito! Agora me diga seu peso atual em kg (ex.: 77.7):", state

    # 2) Peso
    if state.etapa == "peso":
        peso = _parse_float(msg)
        if peso is None or peso <= 0:
            return "Valor de peso inválido. Digite apenas o número em kg (ex.: 77.7):", state
        state.dados["peso"] = peso
        state.etapa = "atividade"
        return (
            "Certo! Agora, em uma escala de 0 a 10, qual é o seu nível de atividade física?\n"
            "0 = totalmente sedentário, 10 = atleta de alta performance."
        ), state

    # 3) Atividade
    if state.etapa == "atividade":
        atv = _parse_int(msg)
        if atv is None or atv < 0 or atv > 10:
            return "Por favor, digite um número inteiro entre 0 e 10 para atividade física:", state
        state.dados["atividade"] = atv
        state.etapa = "colesterol"
        return (
            "Anotado! Se você souber, informe seu colesterol total (mg/dL) "
            "(ex.: 180). Se não souber, pode chutar um valor médio como 180–200:"
        ), state

    # 4) Colesterol
    if state.etapa == "colesterol":
        col = _parse_int(msg)
        if col is None or col <= 0:
            # se o user errar muito, assume um valor padrão
            col = 190
        state.dados["colesterol"] = col
        state.etapa = "n_refeicoes"
        return (
            "Beleza! Quantas refeições principais você gostaria por dia? "
            "(ex.: 3, 4, 5):"
        ), state

    # 5) Número de refeições
    if state.etapa == "n_refeicoes":
        n = _parse_int(msg)
        if n is None or n < 3 or n > 7:
            return "Digite um número de refeições entre 3 e 7 (ex.: 5):", state
        state.dados["n_refeicoes"] = n
        state.etapa = "restricoes"
        return (
            "Você possui alguma restrição ou alimento que não gosta?\n"
            "Ex.: lactose, camarão, glúten. Separe por vírgula.\n"
            "Se não tiver, digite 'nenhuma'."
        ), state

    # 6) Restrições
    if state.etapa == "restricoes":
        restr = _parse_restricoes(msg)
        state.dados["restricoes"] = restr
        state.etapa = "orcamento"
        return (
            "Ótimo! Qual é o orçamento diário aproximado para alimentação "
            "(em reais, ex.: 30)? Se não quiser limitar, digite 0."
        ), state

    # 7) Orçamento
    if state.etapa == "orcamento":
        orc = _parse_float(msg)
        if orc is None or orc < 0:
            return "Valor inválido. Digite apenas o número em reais (ex.: 25.0):", state
        state.dados["orcamento_max"] = orc if orc > 0 else 9999.0

        # Aqui já temos tudo: chama o core_engine
        state.etapa = "gerando"
        try:
            dados_core = {
                "objetivo": state.dados["objetivo"],
                "atividade": state.dados["atividade"],
                "colesterol": state.dados["colesterol"],
                "peso": state.dados["peso"],
                "n_refeicoes": state.dados["n_refeicoes"],
                "restricoes": state.dados["restricoes"],
                "orcamento_max": state.dados["orcamento_max"],
                # Ajuste o caminho da tabela_csv conforme seu projeto
                "tabela_csv": "assets/data/taco_min.csv",
                "ag": {
                    "pop": 120,
                    "ger": 200,
                    "elit": 6,
                    "seed": 42,
                },
            }

            resultado = gerar_plano_para_usuario(dados_core)

            # Tenta usar ChatGPT se a chave existir; senão usa formato bruto
            if os.environ.get("OPENAI_API_KEY"):
                texto = _formatar_plano_com_ia(resultado)
            else:
                texto = _formatar_plano_bruto(resultado)

            state.etapa = "fim"
            return texto, state

        except Exception as e:
            state.etapa = "erro"
            return (
                "Ops, houve um erro ao gerar o plano 😥\n"
                f"Detalhes técnicos: {e}\n"
                "Tente novamente mais tarde ou peça ajuda ao time técnico.",
                state,
            )

    # Depois que o plano já foi gerado
    if state.etapa in ("fim", "erro"):
        if msg.lower() in ("novo", "sim", "s", "gerar outro", "outro"):
            state = ChatState(etapa="inicio", dados={})
            return "Vamos começar um novo plano! ✨\n\n" + MSG_BOAS_VINDAS, state
        else:
            return (
                "Se quiser gerar um novo plano, digite 'novo'.\n"
                "Se quiser encerrar, digite 'sair'.",
                state,
            )

    # Fallback de segurança
    return "Não entendi muito bem. Se quiser recomeçar, digite 'novo'.", state
