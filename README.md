# 🤖 **NutriBotIA – Recomendação Inteligente de Dietas (Fuzzy + AG + Chatbot)**

**NutriBotIA** é um sistema completo de Inteligência Artificial capaz de gerar cardápios personalizados a partir de preferências, objetivos e dados metabólicos do usuário.

Ele combina:

* 🧠 **Lógica Fuzzy** — interpreta fatores subjetivos (atividade, colesterol, objetivo)
* 🧬 **Algoritmos Genéticos** — monta o melhor cardápio possível com base em metas nutricionais
* 🗂️ **Core Engine** — integra Fuzzy + AG + rótulos da dieta
* 💬 **Chatbot (Python + Flask)** — fluxo conversacional estruturado
* 📱 **Bot WhatsApp (Node.js)** — interação em tempo real via WhatsApp
* 🌐 **API REST** — comunicação entre interface e motor de IA
* 📊 **TACO** — base nutricional reduzida com alimentos padronizados

---

# 🚀 **Objetivo**

Auxiliar usuários a organizar uma alimentação saudável, prática e adaptada ao estilo de vida real, considerando:

* Preferências alimentares
* Restrições e alergias
* Orçamento diário
* Número de refeições
* Objetivo (cutting, manutenção, bulking)
* Atividade física
* Colesterol

---

# 🧠 **Arquitetura do Sistema**

```
Usuário (WhatsApp / API / Interface)
           ↓
     Chatbot Engine
           ↓
      Core Engine
   ┌───────────────┐
   │  Lógica Fuzzy  │ → calculo de macros e VET
   │ (skfuzzy)      │
   └───────────────┘
           ↓
   ┌───────────────┐
   │ Algoritmo Gen.│ → geração do cardápio ideal
   │ (seleção, mut. │
   │  crossover)    │
   └───────────────┘
           ↓
  Cardápio otimizado + rótulos + métricas
```

---

# 📂 **Estrutura Atual do Repositório**

```
NutriBotIA/
├── assets/
│   ├── chatbot/
│   │   ├── chatbot_engine.py
│   │   ├── teste_chatbot.py
│   │   └── bot_wwjs.js
│   │
│   ├── api_chat.py
│   ├── core_engine.py
│   │
│   ├── fuzzy_module/
│   │   ├── calcular_macros.py
│   │   ├── calcular_vet.py
│   │   └── __init__.py
│   │
│   ├── genetic_module/
│   │   └── genetic_module.py
│   │
│   └── data/
│       └── taco_min.csv
│
├── app.py                    # script de teste rápido
├── README.md
└── requirements.txt
```

---

# 🔧 **Instalação**

Requisitos:

* Python **3.10+**
* pip instalado
* Node.js (opcional, para WhatsApp Bot)

### 1️⃣ **Clonar o Repositório**

```bash
git clone https://github.com/Edu-Argolo-Guerreiro/NutriBotIA-A3.git
cd NutriBotIA-A3
```

### 2️⃣ **Instalar dependências Python**

```bash
pip install -r requirements.txt
```

### 3️⃣ (**Opcional**) Instalar dependências do bot WhatsApp

```bash
cd assets/chatbot
npm install
```

---

# 📄 **requirements.txt (incluído também dentro do README)**

```txt
pandas
numpy
matplotlib
scikit-fuzzy
scipy
networkx
flask
openai
whatsapp-web.js   # via npm, não via pip
```

> *Observação:* `whatsapp-web.js` é instalado via Node (npm), não via pip.

---

# ▶️ **Como executar cada parte do projeto**

---

## 🧪 **1. Testar o motor principal (Fuzzy + AG)**

```bash
python app.py
```

---

## 🌐 **2. Subir a API Flask (para chatbot e WhatsApp)**

```bash
python assets/chatbot/api_chat.py
```

A API ficará disponível em:

```
http://localhost:5000/mensagem
```

---

## 💬 **3. Chatbot via WhatsApp (Node.js)**

Em outro terminal:

```bash
node assets/chatbot/bot_wwjs.js
```

Escaneie o QR Code no seu celular.

---

## 🧠 **4. Rodar diretamente o módulo fuzzy**

```bash
python assets/fuzzy_module/__init__.py
```

---

# 📜 **Licença**

Projeto desenvolvido para fins educacionais e experimentais no contexto da disciplina A3 - SISTEMA DE CONTROLE E INTELIGENCIA ARTIFICIAL - UNIFACS (UNIVERSIDADE DE SALVADOR).