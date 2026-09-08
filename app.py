import streamlit as st

st.set_page_config(page_title="Roma Estofaria", page_icon="🛋️")

st.title("Roma Estofaria - Simulador")
st.write("Transforme seu estofado com nossos materiais exclusivos.")

# Botão para o cliente enviar a foto
foto_cliente = st.file_uploader("Envie a foto do seu sofá atual:", type=["jpg", "png", "jpeg"])

if foto_cliente is not None:
    st.image(foto_cliente, caption="Seu sofá atual", use_container_width=True)
    st.success("Foto carregada com sucesso!")
    
    st.markdown("---")
    st.subheader("Escolha o Novo Material:")
    
    tipo_material = st.radio(
        "Selecione o tecido desejado:",
        ["Suede", "Bouclé", "Linho", "Sintético"],
        horizontal=True
    )
    
    if tipo_material == "Suede":
        st.write("Cores disponíveis em Suede:")
        cor = st.selectbox("Escolha a cor:", ["Bege Claro", "Cinza Chumbo", "Marrom Chocolate", "Azul Petróleo"])
    elif tipo_material == "Bouclé":
        st.write("Cores disponíveis em Bouclé:")
        cor = st.selectbox("Escolha a cor:", ["Bouclé Cru", "Bouclé Cinza", "Bouclé Verde Oliva", "Bouclé Bege"])
    elif tipo_material == "Linho":
        st.write("Cores disponíveis em Linho:")
        cor = st.selectbox("Escolha a cor:", ["Linho Rústico Cru", "Linho Cinza Claro", "Linho Fendi", "Linho Grafite"])
    else:
        st.write("Cores disponíveis em Sintético:")
        cor = st.selectbox("Escolha a cor:", ["Couro Sintético Preto", "Couro Sintético Caramelo", "Couro Sintético Fendi"])
    
    st.markdown("---")
    st.info(f"✨ Material selecionado: **{tipo_material}** na cor **{cor}**")
    
    if st.button("📲 Solicitar Orçamento no WhatsApp", type="primary"):
        st.success("Tudo pronto! Redirecionando para o atendimento da Roma Estofaria...")
