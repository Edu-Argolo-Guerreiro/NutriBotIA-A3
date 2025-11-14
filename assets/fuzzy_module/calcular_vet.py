# calculo do valor energético total
def calculo_valor_energetico_total(objetivo, peso):
    kcal_kg = 0
    match objetivo:
        case 0:  # cutting
            kcal_kg = 22
        case 1:  # manutenção
            kcal_kg = 30
        case 2:  # bulking
            kcal_kg = 38

    valor_energetico_total = peso * kcal_kg

    return valor_energetico_total
