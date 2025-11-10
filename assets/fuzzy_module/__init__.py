from matplotlib import pyplot as plt
from calcular_prioridade import calcular_prioridade
from constantes import renda, tempo_cozinha, saude_geral, prioridade_nutricional


# Exemplo de Uso (com Visualização)
if __name__ == '__main__':
    print("Visualização das Funções de Pertinência")
    
    # 1. Visualizar as Funções de Pertinência de cada variável
    renda.view()
    tempo_cozinha.view()
    saude_geral.view()
    prioridade_nutricional.view()
    
    plt.show() 

    print("Teste de Simulação (com gráfico)")

    # Exemplo 1: Saúde Delicada e Renda Baixa (Espera-se Prioridade Crítica)
    p2 = calcular_prioridade(renda_val=5, tempo_cozinha_val=5, saude_geral_val=5, mostrar_grafico=True)
    print(f"Renda=5, Tempo=5, Saúde=5 -> Prioridade: {p2:.2f} ")


