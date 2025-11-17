# assets/chatbot/teste_chatbot.py

import os
from chatbot_engine import ChatState, processar_mensagem

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # pasta assets
TABELA_CSV = os.path.join(BASE_DIR, "data", "taco_min.csv")

def loop_chat():
    state = ChatState(etapa="inicio")
    resposta, state = processar_mensagem(state, "")
    print(resposta)

    while not state.terminou:
        msg = input("\nVocê: ")
        resposta, state = processar_mensagem(state, msg)
        print("\nBot:", resposta)

if __name__ == "__main__":
    loop_chat()
