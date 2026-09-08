import streamlit as st

st.set_page_config(page_title="Roma Estofaria", page_icon="🛋️")

st.title("Roma Estofaria - Simulador")
st.write("Bem-vindo ao simulador de estofados.")

foto = st.file_uploader("Envie a foto do seu sofá:", type=["jpg", "png", "jpeg"])

if foto:
    st.image(foto, caption="Foto recebida com sucesso!")
    st.success("Tudo funcionando perfeitamente!")
    
    tecido = st.selectbox("Escolha o tecido:", ["Suede", "Bouclé", "Linho", "Sintético"])
    st.write(Você escolheu: {tecido})
