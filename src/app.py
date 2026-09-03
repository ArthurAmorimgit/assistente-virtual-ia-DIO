import json
import os
from google import genai
from google.genai import types
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configuração da página no Streamlit
st.set_page_config(page_title="Edu - Assistente Financeiro", page_icon="💰")
st.title("💰 Edu - Seu Assistente Financeiro")

# Carrega a base de conhecimento
def carregar_base():
    caminho = os.path.join("data", "conhecimento.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

base_dados = carregar_base()

# Inicializa o cliente da API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Inicializa o histórico no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada do usuário
if user_input := st.chat_input("Como posso te ajudar com suas finanças hoje?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Prepara o contexto
    system_instruction = f"""
    Você é o Edu, um assistente virtual educativo de finanças.
    Base de conhecimento disponível: {json.dumps(base_dados, ensure_ascii=False)}
    
    Instruções:
    1. Responda usando prioritariamente a base de conhecimento.
    2. Se não souber ou não estiver na base, diga educadamente que não possui a informação.
    3. Nunca faça recomendações diretas de compra de ações ou criptomoedas.
    """

    # Chamada do modelo Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        ),
    )

    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)
