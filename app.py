import streamlit as st
import urllib.parse

# Configura a aba do navegador com o nome da loja
st.set_page_config(page_title="Roma Estofaria", page_icon="🛋️")

# Cabeçalho com a identidade da marca
st.title("Roma Estofaria - Simulador")
st.write("Transforme seu estofado com nossos materiais exclusivos.")

# 1. Botão para o cliente enviar a foto do sofá atual
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
    
    # Dicionário com fotos de exemplo gratuitas para cada tecido
    imagens_referencia = {
        "Suede": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80",
        "Bouclé": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=800&q=80",
        "Linho": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=800&q=80",
        "Sintético": "https://images.unsplash.com/photo-1567016432779-094069958ea5?auto=format&fit=crop&w=800&q=80"
    }
    
    # Seleção de cores baseada no material
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
    
    # Exibe a foto de referência visual do tecido escolhido
    st.markdown("### 👁️ Referência do Material:")
    st.image(imagens_referencia[tipo_material], caption=f"Exemplo de acabamento em {tipo_material}", use_container_width=True)
    
    st.markdown("---")
    st.info(f"✨ Material selecionado: **{tipo_material}** na cor **{cor}**")
    
    # Número do WhatsApp da Roma Estofaria (altere depois se precisar)
    numero_whatsapp = "5541999999999" 
    
    mensagem = f"Olá, Roma Estofaria! Gostaria de um orçamento para reformar meu sofá no material {tipo_material} - Cor: {cor}."
    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensagem)}"
    
    # Botão de redirecionamento para o WhatsApp
    st.markdown(
        f'<a href="{link_whatsapp}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; padding:12px; border:none; border-radius:5px; font-size:16px; font-weight:bold; cursor:pointer;">📲 Enviar Orçamento via WhatsApp</button></a>',
        unsafe_allow_html=True
    )
