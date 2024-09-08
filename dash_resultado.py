import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from PIL import Image

# Configuração do acesso ao Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"] 
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("LITTERACI_DB").sheet1

# Função para ler os dados do Google Sheets
@st.cache_data(ttl=600)
def load_data():
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Carregar os dados
df = load_data()

# Processar dados das escalas
def process_scale_data(df, col_name):
    scale_data = df[col_name].apply(lambda x: pd.Series(str(x).split(";")))
    scale_data.columns = [f"{col_name}_{i+1}" for i in range(len(scale_data.columns))]
    scale_data = scale_data.apply(pd.to_numeric)
    return scale_data

situacao_atual_data = process_scale_data(df, "Situacao Atual UI")
situacao_futura_data = process_scale_data(df, "Situacao Futura UI")

# Estilo do dashboard
st.markdown(
    """
    <style>
    :root {
        --primary-color: #A42593;
        --background-color: #F9F9F9;
        --text-color: #000000;
        --font-size-title: 24px;
        --font-size-subtitle: 18px;
    }
    /* Resto do CSS... */
    </style>
    """,
    unsafe_allow_html=True
)

# Título do dashboard
st.title("Dashboard de Análise das Respostas da Pesquisa")

# Filtros
st.sidebar.title("Filtros")
tipo_ui_options = ["Arquivo (setor público)", "Arquivo (setor privado)", "Biblioteca (setor público)", 
                   "Biblioteca (setor privado)", "Museu (setor público)", "Museu (setor privado)", 
                   "Outro tipo de Unidade de Informação"]
tipo_ui_filter = st.sidebar.multiselect("Tipo de UI", options=tipo_ui_options, default=tipo_ui_options)

# Aplicar filtros
filtered_df = df[df["Tipo de UI"].isin(tipo_ui_filter)]
filtered_situacao_atual = situacao_atual_data[df["Tipo de UI"].isin(tipo_ui_filter)]
filtered_situacao_futura = situacao_futura_data[df["Tipo de UI"].isin(tipo_ui_filter)]

# Gráficos e análises
st.header("Visão Geral")
st.write(f"Total de respostas: {len(filtered_df)}")

# Gráfico de pizza - Tipos de UI
tipo_ui_counts = filtered_df["Tipo de UI"].value_counts()
fig_tipo_ui = px.pie(tipo_ui_counts, values=tipo_ui_counts, names=tipo_ui_counts.index, title="Distribuição dos Tipos de UI")
st.plotly_chart(fig_tipo_ui)

# Grid de gráficos - Situação Atual
st.header("Situação Atual")
situacao_atual_cols = [f"Situacao Atual UI_{i+1}" for i in range(len(filtered_situacao_atual.columns))]
st.subheader("Médias das respostas")
col1, col2, col3 = st.columns(3)
for i, col in enumerate(situacao_atual_cols):
    if i % 3 == 0:
        with col1:
            avg_score = filtered_situacao_atual[col].mean().round(2)
            st.metric(label=f"Pergunta {i+1}", value=avg_score)
    elif i % 3 == 1:
        with col2:
            avg_score = filtered_situacao_atual[col].mean().round(2)
            st.metric(label=f"Pergunta {i+1}", value=avg_score)
    else:
        with col3:
            avg_score = filtered_situacao_atual[col].mean().round(2)
            st.metric(label=f"Pergunta {i+1}", value=avg_score)

# Grid de gráficos - Situação Futura
st.header("Situação Futura")
situacao_futura_cols = [f"Situacao Futura UI_{i+1}" for i in range(len(filtered_situacao_futura.columns))]
st.subheader("Médias das respostas")
col1, col2 = st.columns(2)
for i, col in enumerate(situacao_futura_cols):
    if i % 2 == 0:
        with col1:
            avg_score = filtered_situacao_futura[col].mean().round(2)
            st.metric(label=f"Pergunta {i+1}", value=avg_score)
    else:
        with col2:
            avg_score = filtered_situacao_futura[col].mean().round(2)
            st.metric(label=f"Pergunta {i+1}", value=avg_score)

# Opiniões sobre a LITTERACI
st.header("Opiniões sobre a LITTERACI")
opcoes_litteraci = filtered_df["Opinioes UI"].str.split(";", expand=True).apply(pd.Series).stack()
opcoes_litteraci = opcoes_litteraci[opcoes_litteraci != ""]
opiniao_counts = opcoes_litteraci.value_counts()

# Tabela de opiniões
opiniao_df = pd.DataFrame({"Opinião": opiniao_counts.index, "Contagem": opiniao_counts.values})
st.table(opiniao_df)

# Logo
logo = Image.open('images/logo.png')
st.image(logo, width=150, use_column_width=True)

# Atualizar dados
if st.button("Atualizar Dados"):
    df = load_data()
    st.experimental_rerun()