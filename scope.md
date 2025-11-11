# DOCUMENTO DE ESCOPO DO PROJETO - NUTRIBOTIA

## UNIVERSIDADE DE SALVADOR - UNIFACS

Unidade Curricular: Sistemas de Controle e Inteligência Artificial

Curso: Engenharia da Computação

Integrantes: Edu Argôlo, Laís Viana, Sinval Luz, Guilherme Almeida, Eric Lelis

Professor: Adailton de Jesus Cerqueira Junior  
Ano: 2025

### **OBJETIVOS DO PROJETO**

Desenvolver o **NutriBotIA**, um chatbot inteligente para **recomendação personalizada de dietas** com base em fatores subjetivos do usuário, utilizando **Lógica Fuzzy** e **Algoritmos Genéticos**.

**Metas de alto nível:**

- Criar um sistema funcional e explicável de IA sem dependência de APIs externas.
- Gerar dietas otimizadas em custo e valor nutricional.
- Traduzir linguagem informal do usuário em decisões nutricionais coerentes.
- Oferecer uma interface interativa (via Streamlit) e de fácil usabilidade.

**Critérios de sucesso mensuráveis:**

- ≥ 90% de acurácia nas interpretações Fuzzy.
- ≥ 80% de coerência nutricional nas dietas geradas.
- Interface funcional e validada em pelo menos 3 perfis de teste.

---

### **Primeiro Passo – Produtos do Projeto**

| **ENTREGUA Nº** | **DESCRIÇÃO**                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| 1               | `fuzzy_module.py`: módulo de lógica Fuzzy que interpreta variáveis linguísticas (renda, tempo, saúde). |
| 2               | `genetic_module.py`: algoritmo genético que otimiza cardápios com base em custo e nutrientes.          |
| 3               | `main.py`: integração completa do chatbot com interface Streamlit.                                     |
| 4               | `alimentos.csv`: base de dados nutricionais e custos.                                                  |
| 5               | `poster.pdf`: pôster acadêmico com resumo e arquitetura do sistema.                                    |
| 6               | `documentação técnica`: escopo, relatório e README do repositório.                                     |

---

### **Segundo Passo – Lista de Tarefas**

| **TAREFA Nº** | **DESCRIÇÃO**                                            | **ENTREGÁVEL RELACIONADO** |
| ------------- | -------------------------------------------------------- | -------------------------- |
| 1             | Planejamento e definição das variáveis linguísticas      | 1                          |
| 2             | Criação da base nutricional (`alimentos.csv`)            | 4                          |
| 3             | Desenvolvimento do módulo Fuzzy (`fuzzy_module.py`)      | 1                          |
| 4             | Desenvolvimento do módulo Genético (`genetic_module.py`) | 2                          |
| 5             | Integração dos módulos no chatbot (`main.py`)            | 3                          |
| 6             | Testes de validação e refinamento                        | 1–3                        |
| 7             | Criação da documentação e pôster final                   | 5, 6                       |

**Estrutura de divisão de trabalho (WBS):** ✔️ Anexada no repositório GitHub com tag `EntregaA3`.

---

### **Fora do Escopo**

O projeto **NÃO** contempla:

- Monitoramento físico em tempo real (wearables).
- Consultas nutricionais clínicas ou personalizadas por profissionais.
- Suporte a múltiplos idiomas
- Integração com Google Fit

---

### **Hipóteses do Projeto**

| **Nº** | **SUPOSIÇÃO**                                                                            |
| ------ | ---------------------------------------------------------------------------------------- |
| 1      | Os dados nutricionais da base `alimentos.csv` são confiáveis e completos.                |
| 2      | As respostas do usuário seguem padrões linguísticos básicos de compreensão.              |
| 3      | Os parâmetros genéticos (taxas e população) são suficientes para convergência eficiente. |

**Impacto se falsas:** perda de precisão nas recomendações e necessidade de readequação dos módulos de IA.

---

### **Restrições do Projeto**

**DATA DE INÍCIO:** 15/09/2025  
**LANÇAMENTO / GO-LIVE:** 25/10/2025  
**TÉRMINO:** 20/11/2025

**RESTRIÇÕES ORÇAMENTÁRIAS:**

- Sem custos diretos; uso apenas de ferramentas open source (Python, DEAP, scikit-fuzzy, Streamlit).

**RESTRIÇÕES DE QUALIDADE / DESEMPENHO:**

- Respostas do chatbot devem ocorrer em ≤ 3 segundos.
- Erro máximo de 10% nas calorias totais recomendadas.

**RESTRIÇÕES DE EQUIPAMENTO / PESSOAL:**

- Equipe de 5 integrantes; cada módulo dividido por função.
- Execução local sem servidores externos.

**RESTRIÇÕES REGULATÓRIAS:**

- Projeto acadêmico, sem coleta de dados pessoais sensíveis.
- Cumprimento da LGPD em simulações de dados.

---
### **Fluxogramas do Projeto

**Macrofluxo** 
- Fluxo linear do sistema:  
	**Usuário → Chatbot → Fuzzy → AG → Recomendação → Feedback**

<img width="3990" height="391" alt="image" src="https://github.com/user-attachments/assets/0553edca-75de-471e-a1e7-3e36b56af4e1" />

- Fluxo Técnico Detalhado

<img width="2005" height="779" alt="image" src="https://github.com/user-attachments/assets/88c13207-977b-465e-8b4f-ddefb899e510" />


---

### **Estimativas Atualizadas**

**Estimativa total:** 120 horas

- Desenvolvimento Fuzzy: 25h
    
- Desenvolvimento Genético: 30h
    
- Integração e Interface: 35h
    
- Testes e Documentação: 30h
    

---

### **Aprovações**

| **NOME / TÍTULO**               | **FUNÇÃO / APROVADOR** | **DATA ENVIADA** | **DATA APROVADA** |     |
| ------------------------------- | ---------------------- | ---------------- | ----------------- | --- |
| Prof. Adailton Cerqueira Junior | Orientador / Avaliador | 18/11/2025       |                   |     |
|                                 |                        |                  |                   |     |
