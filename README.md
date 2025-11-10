# 🤖 NutriBotIA – Recomendação Inteligente de Dietas

**NutriBotIA** é um chatbot desenvolvido com técnicas de Inteligência Artificial para recomendar cardápios personalizados considerando:

✅ Renda  
✅ Tempo disponível  
✅ Preferências alimentares  
✅ Restrições/alergias  
✅ Metas nutricionais

O projeto utiliza:

- **Lógica Fuzzy** — para interpretar fatores subjetivos do usuário
- **Algoritmos Genéticos** — para otimizar o cardápio ideal
- **Chatbot (Streamlit)** — interface amigável acessível pelo navegador

---

## 🚀 Objetivo

Auxiliar usuários na organização de uma alimentação saudável e acessível, alinhada ao seu estilo de vida.

---

## 🧠 Arquitetura

Usuário → Chatbot → Módulo Fuzzy → Algoritmo Genético → Dieta Recomendada

---

## 📂 Estrutura do repositório

NutriBotIA/
├── data/
│ └── alimentos.csv
├── src/
│ ├── fuzzy_module.py
│ ├── genetic_module.py
│ └── main.py
├── docs/
│ └── poster.pdf
├── README.md
└── requirements.txt

---

## 🔧 Instalação

Requisitos:

- Python 3.12
- pip instalado

```bash
pip install -r requirements.txt
```

## Programa fuzzy

```bash
python .\assets\fuzzy_module\__init__.py
```
