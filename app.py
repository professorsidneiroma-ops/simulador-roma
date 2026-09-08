import streamlit as st

# Configura a aba do navegador com o nome da loja
st.set_page_config(page_title="Roma Estofaria", page_icon="🛋️")

# Título e texto de boas-vindas
st.title("Roma Estofaria - Simulador 3D")
st.write("Veja como seu estofado vai ficar com nossos materiais exclusivos (Suede, Bouclé, Linho ou Sintético).")

# Cria o botão para o cliente enviar a foto
foto_cliente = st.file_uploader("Tire uma foto do seu sofá ou envie da galeria:", type=["jpg", "png", "jpeg"])

# Mostra a foto na tela se o cliente enviou algo
if foto_cliente:
    st.image(foto_cliente, caption="Recebemos a foto do seu sofá!")
    st.success("Imagem carregada! Preparando os tecidos...")
