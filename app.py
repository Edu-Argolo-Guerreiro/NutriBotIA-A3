from assets.fuzzy_module import calcular_macros


carboidratos, proteina, gordura = calcular_macros(2, 7, 20, 77.7)

print("=== RESULTADOS FUZZY ===")
print(f"Carboidratos: {carboidratos} g")
print(f"Proteínas: {proteina} g")
print(f"Gorduras: {gordura} g")
