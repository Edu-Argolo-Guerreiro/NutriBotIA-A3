from matplotlib import pyplot as plt
from .constantes import *                  # <- COM ponto
from .regras import simulador_prioridade   # <- COM ponto


# Implementação da Função Principal 
def calcular_prioridade(renda_val: float, tempo_cozinha_val: float, saude_geral_val: float, mostrar_grafico: bool = False) -> float:
    """
    Calcula o nível de prioridade nutricional (0 a 10) utilizando lógica fuzzy e,
    opcionalmente, exibe o gráfico de ativação da saída.
    """
    try:
        simulador_prioridade.input["renda"] = renda_val
        simulador_prioridade.input["tempo_cozinha"] = tempo_cozinha_val
        simulador_prioridade.input["saude_geral"] = saude_geral_val

        simulador_prioridade.compute()

        prioridade = simulador_prioridade.output["prioridade_nutricional"]

        if mostrar_grafico:
            print("Visualização da Saída Fuzzy")

            # mostra a defuzzificação e as ativações das regras.
            prioridade_nutricional.view(sim=simulador_prioridade)
            plt.show()

        return prioridade

    except ValueError as e:
        print(f"Erro ao computar prioridade: {e}")
        return 0.0