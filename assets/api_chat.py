# api_chat.py
"""
API REST do NutriBotIA
----------------------

Este módulo expõe uma rota HTTP simples para comunicação com o chatbot,
permitindo que clientes (Web, Mobile ou CLI) enviem mensagens e recebam
respostas processadas pelo ChatState e pelo motor de diálogo.

Fluxo:
1. Cliente envia JSON contendo "user_id" e "texto" para /mensagem
2. O estado de conversa desse usuário é recuperado (ou criado se for novo)
3. A mensagem é processada pelo chatbot_engine
4. O estado atualizado é salvo em memória
5. A resposta é devolvida como JSON

Observação:
- O armazenamento de estado é feito em memória e não é persistente.
- Em produção, recomenda-se substituir por Redis, banco ou session store.
"""

# ---------------------------------------------------------------------------
# Comentários e ajustes inseridos com auxílio do ChatGPT (GPT-5.1 Thinking)
# Data: 2025-11-19
# ---------------------------------------------------------------------------

from flask import Flask, request, jsonify
from chatbot.chatbot_engine import ChatState, processar_mensagem

app = Flask(__name__)

# ---------------------------------------------------------------------------
# ARMAZENAMENTO DOS ESTADOS
# ---------------------------------------------------------------------------
# Cada usuário tem um ChatState próprio.
# Aqui usamos um dicionário simples (em memória) mapeando user_id → ChatState.
# Isso funciona bem para testes locais, mas não escala em produção.
estados = {}


# ---------------------------------------------------------------------------
# ROTA PRINCIPAL DO CHATBOT
# ---------------------------------------------------------------------------
@app.route("/mensagem", methods=["POST"])
def mensagem():
    """
    Entrada:
        {
            "user_id": "usuario123",
            "texto": "Olá, quero montar uma dieta"
        }

    Lógica:
    - Recupera ou cria o estado do usuário
    - Processa a mensagem usando o motor de diálogo (chatbot_engine)
    - Atualiza o estado
    - Devolve apenas o texto da resposta

    Saída:
        {
            "resposta": "...",
        }
    """
    data = request.get_json() or {}

    # user_id identifica a conversa; se não houver, usamos "anonimo"
    user_id = data.get("user_id", "anonimo")
    texto = data.get("texto", "")

    # Obtém o estado existente ou inicializa um novo
    state = estados.get(user_id, ChatState(etapa="inicio", dados={}))

    # processar_mensagem devolve (texto_resposta, novo_estado)
    resposta, novo_state = processar_mensagem(state, texto)

    # Armazena o estado atualizado
    estados[user_id] = novo_state

    # Retorna somente a resposta (mínimo necessário para o cliente)
    return jsonify({"resposta": resposta})


# ---------------------------------------------------------------------------
# EXECUÇÃO DA API (MODO LOCAL)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("API NutriBot rodando em http://localhost:5000")
    # debug=True para recarregar automaticamente durante desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)
