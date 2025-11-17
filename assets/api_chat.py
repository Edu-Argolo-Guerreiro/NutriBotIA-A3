# api_chat.py
from flask import Flask, request, jsonify
from assets.chatbot.chatbot_engine import ChatState, processar_mensagem

app = Flask(__name__)

# Estados de conversa na RAM (chave = id do usuário no WhatsApp)
user_states = {}

def get_state(user_id: str) -> ChatState:
    if user_id not in user_states:
        user_states[user_id] = ChatState()
    return user_states[user_id]


@app.route("/mensagem", methods=["POST"])
def mensagem():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    texto = data.get("texto", "")

    if not user_id:
        return jsonify({"erro": "user_id não enviado"}), 400

    state = get_state(user_id)
    resposta, novo_state = processar_mensagem(state, texto)
    user_states[user_id] = novo_state

    return jsonify({"resposta": resposta})


if __name__ == "__main__":
    # roda em http://localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
