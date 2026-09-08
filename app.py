import base64
import urllib.parse

import requests
import streamlit as st


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Roma Estofaria - Simulador",
    page_icon="🛋️",
    layout="centered"
)


# ESTILO VISUAL
st.markdown(
    """
    <style>
        .stApp {
            background-color: #111111;
            color: #ffffff;
        }

        h1, h2, h3 {
            color: #d4af37 !important;
        }

        .stButton > button {
            width: 100%;
            background-color: #d4af37;
            color: #111111;
            border: none;
            font-weight: bold;
            padding: 12px;
            border-radius: 8px;
        }

        .stDownloadButton > button {
            width: 100%;
            background-color: #d4af37;
            color: #111111;
            border: none;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Roma Estofaria")
st.subheader("Simulador Virtual de Reforma")

st.write(
    "Envie a foto do estofado e uma fotografia do tecido que deseja aplicar."
)


# UPLOAD DAS IMAGENS
foto_sofa = st.file_uploader(
    "1. Envie a foto do sofá, poltrona ou estofado:",
    type=["jpg", "jpeg", "png"],
    key="foto_sofa"
)

foto_tecido = st.file_uploader(
    "2. Envie a foto do tecido escolhido:",
    type=["jpg", "jpeg", "png"],
    key="foto_tecido"
)


# ESCOLHA DO MATERIAL
tipo_material = st.selectbox(
    "3. Escolha o tipo de material:",
    ["Suede", "Bouclé", "Linho", "Sintético", "Outro"]
)

cor_material = st.text_input(
    "4. Informe a cor:",
    placeholder="Exemplo: areia, preto, cinza-claro ou caramelo"
)


# MOSTRAR AS DUAS IMAGENS
if foto_sofa is not None and foto_tecido is not None:
    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.image(
            foto_sofa,
            caption="Estofado original",
            use_container_width=True
        )

    with coluna2:
        st.image(
            foto_tecido,
            caption="Tecido escolhido",
            use_container_width=True
        )


# FUNÇÃO QUE ENVIA AS IMAGENS PARA A IA
def gerar_simulacao(imagem_sofa, imagem_tecido, material, cor):
    api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "A chave OPENAI_API_KEY ainda não foi configurada no Streamlit."
        )

    imagem_sofa.seek(0)
    imagem_tecido.seek(0)

    tipo_sofa = imagem_sofa.type or "image/jpeg"
    tipo_tecido = imagem_tecido.type or "image/jpeg"

    arquivos = [
        (
            "image[]",
            (
                imagem_sofa.name,
                imagem_sofa.getvalue(),
                tipo_sofa
            )
        ),
        (
            "image[]",
            (
                imagem_tecido.name,
                imagem_tecido.getvalue(),
                tipo_tecido
            )
        )
    ]

    prompt = f"""
A primeira imagem mostra o estofado original do cliente.
A segunda imagem mostra a referência exata do tecido.

Produza uma simulação fotográfica realista da reforma do estofado da
primeira imagem, aplicando o material {material}, na cor {cor}.

A segunda imagem deve ser usada como referência fiel de cor, textura,
trama, brilho e acabamento.

Regras obrigatórias:

1. Manter exatamente o modelo original do estofado.
2. Não alterar formato, proporções, tamanho ou perspectiva.
3. Manter a quantidade e a posição dos módulos.
4. Manter braços, assentos, encostos, almofadas e pés.
5. Preservar as costuras e divisões originais.
6. Não criar debrum nem costura dupla onde não existe.
7. Não modificar paredes, piso, objetos ou iluminação do ambiente.
8. Alterar somente o revestimento estofado.
9. Preservar sombras, dobras, volumes e iluminação natural.
10. Não adicionar textos, preços, pessoas ou objetos.
11. O resultado deve parecer uma fotografia verdadeira de um serviço
concluído pela Roma Estofaria.
"""

    dados = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "quality": "medium",
        "size": "auto",
        "input_fidelity": "high",
        "output_format": "jpeg",
        "output_compression": "90"
    }

    cabecalho = {
        "Authorization": f"Bearer {api_key}"
    }

    resposta = requests.post(
        "https://api.openai.com/v1/images/edits",
        headers=cabecalho,
        data=dados,
        files=arquivos,
        timeout=180
    )

    if resposta.status_code != 200:
        try:
            erro = resposta.json()
            mensagem = erro.get("error", {}).get(
                "message",
                "Não foi possível gerar a simulação."
            )
        except Exception:
            mensagem = resposta.text

        raise RuntimeError(mensagem)

    resultado = resposta.json()

    if not resultado.get("data"):
        raise RuntimeError("A inteligência artificial não devolveu uma imagem.")

    imagem_base64 = resultado["data"][0]["b64_json"]
    return base64.b64decode(imagem_base64)


# BOTÃO PARA GERAR
pode_gerar = (
    foto_sofa is not None
    and foto_tecido is not None
    and cor_material.strip() != ""
)

if st.button(
    "Gerar simulação da reforma",
    type="primary",
    disabled=not pode_gerar
):
    try:
        with st.spinner(
            "Aplicando o tecido ao estofado. Isso pode levar até dois minutos..."
        ):
            resultado_imagem = gerar_simulacao(
                foto_sofa,
                foto_tecido,
                tipo_material,
                cor_material
            )

        st.session_state["resultado_imagem"] = resultado_imagem
        st.success("Simulação concluída!")

    except Exception as erro:
        st.error(f"Não foi possível gerar a simulação: {erro}")


# MOSTRAR O RESULTADO
if "resultado_imagem" in st.session_state:
    resultado = st.session_state["resultado_imagem"]

    st.markdown("---")
    st.subheader("Resultado da reforma")

    coluna_antes, coluna_depois = st.columns(2)

    with coluna_antes:
        foto_sofa.seek(0)
        st.image(
            foto_sofa,
            caption="Antes",
            use_container_width=True
        )

    with coluna_depois:
        st.image(
            resultado,
            caption="Simulação da reforma",
            use_container_width=True
        )

    st.download_button(
        "Baixar a simulação",
        data=resultado,
        file_name="simulacao_roma_estofaria.jpg",
        mime="image/jpeg"
    )

    numero_whatsapp = "5541999999999"

    mensagem = (
        "Olá, Roma Estofaria! Fiz uma simulação de reforma "
        f"em {tipo_material}, na cor {cor_material}, e gostaria "
        "de solicitar um orçamento."
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
        "Baixe a simulação e envie a imagem durante o atendimento pelo WhatsApp."
    )
