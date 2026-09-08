import io
import urllib.parse

import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from rembg import remove


st.set_page_config(
    page_title="Roma Estofaria - Simulador",
    page_icon="🛋️",
    layout="centered"
)


# Aparência do site
st.markdown(
    """
    <style>
        .stApp {
            background-color: #111111;
            color: white;
        }

        h1, h2, h3 {
            color: #d4af37 !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            width: 100%;
            background-color: #d4af37;
            color: #111111;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Roma Estofaria")
st.subheader("Simulador Virtual de Reforma")

st.write(
    "Envie a fotografia do estofado e depois a fotografia do tecido."
)


# Recebimento das imagens
foto_sofa = st.file_uploader(
    "1. Envie a foto do sofá, poltrona ou puff:",
    type=["jpg", "jpeg", "png"],
    key="sofa"
)

foto_tecido = st.file_uploader(
    "2. Envie uma foto aproximada do tecido:",
    type=["jpg", "jpeg", "png"],
    key="tecido"
)


material = st.selectbox(
    "3. Escolha o material:",
    ["Suede", "Bouclé", "Linho", "Sintético", "Outro"]
)

intensidade = st.slider(
    "Intensidade da aplicação:",
    min_value=40,
    max_value=100,
    value=85,
    step=5
)


def preparar_imagem(arquivo):
    imagem = Image.open(arquivo)
    imagem = ImageOps.exif_transpose(imagem)
    imagem = imagem.convert("RGB")

    # Limita o tamanho para não pesar no Streamlit
    imagem.thumbnail((1400, 1400), Image.Resampling.LANCZOS)

    return imagem


def criar_textura_repetida(textura, tamanho):
    largura, altura = tamanho

    textura = textura.convert("RGB")
    textura = ImageEnhance.Color(textura).enhance(1.08)
    textura = ImageEnhance.Contrast(textura).enhance(1.08)

    largura_bloco = max(220, largura // 3)

    proporcao = largura_bloco / textura.width
    altura_bloco = max(1, int(textura.height * proporcao))

    bloco = textura.resize(
        (largura_bloco, altura_bloco),
        Image.Resampling.LANCZOS
    )

    resultado = Image.new("RGB", (largura, altura))

    for y in range(0, altura, bloco.height):
        for x in range(0, largura, bloco.width):
            resultado.paste(bloco, (x, y))

    return resultado


def aplicar_tecido(imagem_original, imagem_tecido, intensidade_aplicacao):
    largura, altura = imagem_original.size

    # Recorta automaticamente o objeto principal
    imagem_rgba = remove(imagem_original).convert("RGBA")
    mascara = imagem_rgba.getchannel("A")

    # Suaviza as bordas do recorte
    mascara = mascara.filter(ImageFilter.GaussianBlur(radius=1.2))

    textura = criar_textura_repetida(
        imagem_tecido,
        (largura, altura)
    )

    original_np = np.asarray(imagem_original).astype(np.float32) / 255.0
    textura_np = np.asarray(textura).astype(np.float32) / 255.0

    # Calcula luminosidade original para preservar sombras e volumes
    luminosidade = (
        original_np[:, :, 0] * 0.299
        + original_np[:, :, 1] * 0.587
        + original_np[:, :, 2] * 0.114
    )

    imagem_cinza = Image.fromarray(
        np.uint8(np.clip(luminosidade * 255, 0, 255))
    )

    # Descobre os detalhes finos: dobras, botões e costuras
    imagem_suave = imagem_cinza.filter(
        ImageFilter.GaussianBlur(radius=8)
    )

    cinza_np = np.asarray(imagem_cinza).astype(np.float32) + 1
    suave_np = np.asarray(imagem_suave).astype(np.float32) + 1

    detalhes = np.clip(cinza_np / suave_np, 0.70, 1.30)

    # Mantém as sombras, mas evita que tecidos claros fiquem escuros demais
    sombra = np.clip(0.55 + luminosidade * 0.70, 0.40, 1.15)
    sombra = sombra * detalhes

    tecido_aplicado = textura_np * sombra[:, :, None]
    tecido_aplicado = np.clip(tecido_aplicado, 0, 1)

    intensidade_decimal = intensidade_aplicacao / 100

    # Mistura parte da foto original para preservar costuras
    simulacao_np = (
        tecido_aplicado * intensidade_decimal
        + original_np * (1 - intensidade_decimal)
    )

    simulacao_np = np.uint8(
        np.clip(simulacao_np * 255, 0, 255)
    )

    simulacao = Image.fromarray(simulacao_np).convert("RGB")

    # Aplica somente na área identificada como móvel
    resultado = imagem_original.copy()
    resultado.paste(simulacao, (0, 0), mascara)

    return resultado


if foto_sofa is not None and foto_tecido is not None:
    imagem_sofa = preparar_imagem(foto_sofa)
    imagem_tecido = preparar_imagem(foto_tecido)

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.image(
            imagem_sofa,
            caption="Estofado original",
            use_container_width=True
        )

    with coluna2:
        st.image(
            imagem_tecido,
            caption="Tecido escolhido",
            use_container_width=True
        )

    if st.button("Gerar simulação gratuita", type="primary"):
        try:
            with st.spinner(
                "Identificando o móvel e aplicando o tecido..."
            ):
                resultado = aplicar_tecido(
                    imagem_sofa,
                    imagem_tecido,
                    intensidade
                )

                arquivo_resultado = io.BytesIO()
                resultado.save(
                    arquivo_resultado,
                    format="JPEG",
                    quality=92
                )

                st.session_state["resultado"] = (
                    arquivo_resultado.getvalue()
                )

            st.success("Simulação concluída!")

        except Exception as erro:
            st.error(
                "Não foi possível processar esta imagem. "
                f"Detalhes: {erro}"
            )


if "resultado" in st.session_state:
    resultado_bytes = st.session_state["resultado"]

    st.markdown("---")
    st.subheader("Resultado da simulação")

    st.image(
        resultado_bytes,
        caption=f"Simulação em {material}",
        use_container_width=True
    )

    st.download_button(
        "Baixar simulação",
        data=resultado_bytes,
        file_name="simulacao_roma_estofaria.jpg",
        mime="image/jpeg"
    )

    numero_whatsapp = "5541999999999"

    mensagem = (
        "Olá, Roma Estofaria! Fiz uma simulação de reforma "
        f"no material {material} e gostaria de solicitar um orçamento."
    )

    link_whatsapp = (
        f"https://wa.me/{numero_whatsapp}"
        f"?text={urllib.parse.quote(mensagem)}"
    )

    st.link_button(
        "Solicitar orçamento pelo WhatsApp",
        link_whatsapp,
        use_container_width=True
    )


st.caption(
    "Simulação visual aproximada. A tonalidade pode variar conforme "
    "a iluminação, a tela e o lote do tecido."
)
