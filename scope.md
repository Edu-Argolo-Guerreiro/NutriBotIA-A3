DOCUMENTO DE ESCOPO — NutriBotIA

## **1. Visão Geral do Projeto**

O NutriBotIA é um sistema inteligente para geração de dietas personalizadas, combinando **Lógica Fuzzy**, **Algoritmo Genético (AG)** e um módulo integrador denominado **core_engine**. Seu objetivo é interpretar informações subjetivas do usuário (como rotina, saúde e objetivos) e transformá-las em metas nutricionais claras, que posteriormente são otimizadas pelo AG para produzir cardápios completos, realistas e adaptados ao perfil individual.

A solução foi projetada para fornecer **dietas consistentes**, **nutricionalmente equilibradas**, com **respeito a restrições alimentares** e aderência a porções reais. Além disso, o sistema é modular, escalável e totalmente desenvolvido em Python, permitindo integração direta com chatbots e interfaces interativas.

---

## **2. Problema a ser Resolvido**

Usuários frequentemente possuem dificuldades em criar dietas adequadas para seus objetivos, especialmente quando lidam com **informações vagas**, limitações de tempo, preferências pessoais e metas nutricionais difíceis de interpretar. Métodos tradicionais de recomendação não conseguem transformar essas variáveis subjetivas em cardápios otimizados. O NutriBotIA resolve esse problema combinando interpretação fuzzy com otimização genética.

---

## **3. Metodologia para Aplicação da Solução**

A solução segue uma abordagem híbrida: primeiro, a **Lógica Fuzzy** converte dados incertos ou linguísticos — como nível de atividade, objetivo, percepção de saúde e restrições — em metas nutricionais precisas (carboidratos, proteínas, gorduras e calorias totais). Em seguida, essas metas alimentam um **Algoritmo Genético**, que gera cardápios variados e realistas, avaliados por uma função de fitness robusta com múltiplos critérios nutricionais.

O módulo **core_engine** integra os dois sistemas, garantindo linearidade no fluxo: interpretação → meta nutricional → otimização → escala final → formatação de saída. O desenvolvimento utiliza princípios incrementais, testes contínuos e ajustes finos de parâmetros (mutação, penalizações e limites de porção) para garantir qualidade e coerência nas dietas geradas.

---

## **4. Escopo do Sistema**

### **4.1 Entradas**

- Dados gerais do usuário (idade, peso, altura, objetivo).
    
- Nível de atividade física (termos linguísticos).
    
- Condições como colesterol, hábitos, percepções pessoais (variáveis fuzzy).
    
- Restrições alimentares (intolerâncias, alergias, alimentos banidos).
    
- Base de alimentos (FoodItem) com macros, preços e tags.
    

### **4.2 Processamento**

1. Fuzzificação das variáveis subjetivas.
    
2. Inferência fuzzy para determinar metas nutricionais.
    
3. Geração de populações iniciais (AG).
    
4. Avaliação por função de fitness.
    
5. Seleção, mutação, crossover e evolução.
    
6. Ajuste global de calorias (escala).
    
7. Formatação final da solução em estrutura amigável.
    

### **4.3 Saídas**

- Cardápio diário com refeições detalhadas.
    
- Quantidades exatas por alimento (gramas).
    
- Valores totais: kcal, carboidratos, proteínas, gorduras.
    
- Rótulo da dieta (hipo/normo/hipercalórica, alto carbo/proteína, etc.).
    
- Explicação textual para integração com chatbot.
    
- Log da otimização.
    

### **4.4 Fora do Escopo**

- Cálculo de micronutrientes (ferro, cálcio, vitaminas).
    
- Recomendações de suplementos.
    
- Avaliação clínica profissional.
    
- Interface gráfica complexa (apenas chatbot simples).
    
- Controle de histórico prolongado do usuário.
    

---

## **5. Objetivo do Projeto**

Desenvolver um sistema de recomendação nutricional personalizado que una Lógica Fuzzy e Algoritmo Genético para transformar dados subjetivos em cardápios reais, saudáveis e otimizados, de forma transparente, interpretável e eficiente.

---

## **6. Requisitos**

### **6.1 Requisitos Funcionais (RF)**

**RF01.** O sistema deve interpretar variáveis linguísticas via módulo fuzzy.  
**RF02.** O sistema deve calcular metas nutricionais (kcal, carb_g, prot_g, fat_g).  
**RF03.** O AG deve gerar cardápios completos com 4–6 refeições.  
**RF04.** A função de fitness deve avaliar cada indivíduo considerando:  
 • metas nutricionais  
 • densidade calórica  
 • refeições fracas  
 • variedade  
 • custo  
 • restrições alimentares  
**RF05.** O sistema deve aplicar ajuste global de calorias ao resultado final.  
**RF06.** O core_engine deve integrar fuzzy + AG e retornar estrutura final.  
**RF07.** O chatbot deve exibir dieta, metas e justificativas.  
**RF08.** O sistema deve impedir soluções irreais (porções exageradas).  
**RF09.** O sistema deve suportar banimentos de alimentos individuais.

### **6.2 Requisitos Não Funcionais (RNF)**

**RNF01.** O sistema deve ser totalmente executável em Python.  
**RNF02.** A solução deve ser modular e escalável.  
**RNF03.** Os tempos de execução devem ser compatíveis com uso em chatbot.  
**RNF04.** O código deve ser legível, comentado e versionado no GitHub.  
**RNF05.** Os resultados devem ser reprodutíveis.  
**RNF06.** O sistema deve ser interpretável e explicável.
**RNF07.** O sistema deve atingir ao menos 80% de acurácia técnica na geração dos cardápios.

---

## **7. Fluxograma (Pipeline Detalhado)**

`Usuário    ↓ Chatbot (Interface Streamlit)    ↓ Coleta de dados → Pré-processamento    ↓ Módulo Fuzzy    ├── Fuzzificação    ├── Inferência (regras fuzzy)    └── Defuzzificação → metas nutricionais (carb_g, prot_g, fat_g, kcal)    ↓ Core Engine (orquestração)    ├── define targets    ├── prepara parâmetros    └── chama AG    ↓ Módulo Genético    ├── geração da população inicial    ├── avaliação por fitness    ├── seleção por torneio    ├── crossover    ├── mutação inteligente    └── melhor indivíduo    ↓ Ajuste Global de Calorias (escala)    ↓ Formatação e rótulos nutricionais    ↓ Chatbot → Exibe cardápio + explicações`

---

## **8. Técnicas de IA Utilizadas**

### **Lógica Fuzzy**

- Conversão de linguagem subjetiva em valores numéricos.
    
- Uso de funções de pertinência.
    
- Regras fuzzy para inferência nutricional.
    
- Defuzzificação para metas precisas.
    

### **Algoritmo Genético**

- Representação de indivíduos como refeições.
    
- População inicial realista.
    
- Função de fitness complexa e multiobjetivo.
    
- Seleção por torneio.
    
- Mutação inteligente com limites de porção.
    
- Crossover simples.
    
- Escalonamento final para calorias desejadas.
    

### **Integração (Core Engine)**

- Pipeline fuzzy → AG.
    
- Construção das metas nutricionais.
    
- Montagem do resultado em alto nível.
    

---

## **9. Técnica de Aprendizado de Máquina**

O projeto **não utiliza Machine Learning no sentido tradicional (treinamento supervisionado)**.  
Ele aplica técnicas de **Inteligência Artificial Clássica**, especificamente:

- **Sistemas Fuzzy** — baseados em regras.
    
- **Computação Evolucionária** — AGs.
    

Não há treinamento de modelos com dados rotulados.  
É um sistema explicável, determinístico e orientado por conhecimento.

---

## **10. Entregáveis**

|Entregável|Descrição|Tipo|
|---|---|---|
|alimentos.csv|Base nutricional com valores de 100g|Dados|
|fuzzy_module.py|Implementação completa do sistema fuzzy|Código|
|genetic_module.py|Implementação completa do AG|Código|
|core_engine.py|Orquestração fuzzy + AG|Código|
|main.py|Chatbot + interface|Código|
|escopo.docx/pdf|Documento de escopo|Documento|
|poster.pdf|Banner de apresentação|Documento|
|repositório GitHub|Código final com tag _EntregaA3_|Repositório|

---

## **11. Conclusão do Projeto**

O NutriBotIA demonstra a aplicação integrada de duas abordagens clássicas de Inteligência Artificial, permitindo a criação de dietas realmente personalizadas, explicáveis e alinhadas ao comportamento humano real. A combinação de lógica fuzzy com otimização genética possibilita interpretar imprecisões, gerar soluções otimizadas e manter realismo nutricional. O projeto reforça o potencial da IA clássica como ferramenta prática, ética e de grande utilidade social.
