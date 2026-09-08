import streamlit as st

# Configura a aba do navegador com o nome da loja
st.set_page_config(page_title="Roma Estofaria", page_icon="🛋️")

# Cabeçalho com a identidade da marca
st.title("Roma Estofaria - Simulador")
st.write("Transforme seu estofado com nossos materiais exclusivos.")

# 1. Botão para o cliente enviar a foto
foto_cliente = st.file_uploader("Envie a foto do seu sofá atual:", type=["jpg", "png", "jpeg"])

# Se o cliente enviou a foto, o app avança para a escolha dos tecidos
if foto_cliente:
    st.image(foto_cliente, caption="Seu sofá atual", use_column_width=True)
    st.success("Foto carregada com sucesso!")
    
    st.markdown("---")
    st.subheader("Escolha o Novo Material:")
    
    # Abas de materiais que a Roma Estofaria trabalha
    tipo_material = st.radio(
        "Selecione o tecido desejado:",
        ["Suede", "Bouclé", "Linho", "Sintético"],
        horizontal=True
    )
    
    # Exibe as cores de acordo com o material escolhido
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
    
    # Simulação simulada de resultado
    st.info(f"✨ Material selecionado: **{tipo_material}** na cor **{cor}**")
    
    # Botão de Orçamento para o WhatsApp da Roma Estofaria
    # Substitua o número abaixo pelo WhatsApp real da estofaria (com DDD)
    numero_whatsapp = "5541999999999" 
    mensagem = f"Olá, Roma Estofaria! Gostaria de um orçamento para reformar meu sofá no material {tipo_material} - Cor: {cor}."
    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensagem)}" if 'urllib' in globals() else f"https://wa.me/{numero_whatsapp}"

    if st.button("📲 Solicitar Orçamento no WhatsApp", type="primary"):
        st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/5541999999999?text=Ola%20Roma%20Estofaria,%20gostaria%20de%20orcamento%20para%20reforma.">', unsafe_allow_html=True)
        st.success("Redirecionando para o WhatsApp da Roma Estofaria...")
