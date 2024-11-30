import streamlit as st

# Título do App
st.title("Meu Primeiro App com Streamlit")

# Entrada de texto
nome = st.text_input("Qual é o seu nome?")

# Botão para exibir mensagem
if st.button("Enviar"):
    st.write(f"Olá, {nome}! Bem-vindo ao Streamlit!")
