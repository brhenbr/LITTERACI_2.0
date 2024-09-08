import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

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

# Título do dashboard
st.title("Dashboard de Análise das Respostas da Pesquisa")

# Filtros
st.sidebar.title("Filtros")
tipo_ui_filter = st.sidebar.multiselect("Tipo de UI", options=df["Tipo de UI"].unique(), default=df["Tipo de UI"].unique())

# Aplicar filtros
filtered_df = df[df["Tipo de UI"].isin(tipo_ui_filter)]

# Gráficos e análises
st.header("Visão Geral")
st.write(f"Total de respostas: {len(filtered_df)}")

# Gráfico de pizza - Tipos de UI
tipo_ui_counts = filtered_df["Tipo de UI"].value_counts()
fig_tipo_ui = px.pie(tipo_ui_counts, values=tipo_ui_counts, names=tipo_ui_counts.index, title="Distribuição dos Tipos de UI")
st.plotly_chart(fig_tipo_ui)

# Gráficos de barras - Situação Atual e Futura
st.header("Situação Atual e Futura")

# Processar dados das escalas
situacao_atual_cols = [col for col in df.columns if col.startswith("Situação Atual")]
situacao_futura_cols = [col for col in df.columns if col.startswith("Situação Futura")]

situacao_atual_data = filtered_df[situacao_atual_cols].apply(lambda x: pd.Series(str(x).split(";")).astype(float).mean())
situacao_futura_data = filtered_df[situacao_futura_cols].apply(lambda x: pd.Series(str(x).split(";")).astype(float).mean())

# Gráficos de barras
fig_atual = px.bar(situacao_atual_data, x=situacao_atual_data.index, y=situacao_atual_data, title="Média das Respostas - Situação Atual")
fig_futura = px.bar(situacao_futura_data, x=situacao_futura_data.index, y=situacao_futura_data, title="Média das Respostas - Situação Futura") 

st.plotly_chart(fig_atual)
st.plotly_chart(fig_futura)

# Opiniões sobre a LITTERACI
st.header("Opiniões sobre a LITTERACI")
opcoes_litteraci = filtered_df["Opinioes UI"].str.split(";", expand=True).apply(pd.Series).stack()
opcoes_litteraci = opcoes_litteraci[opcoes_litteraci != ""]

opiniao_counts = opcoes_litteraci.value_counts()

fig_opiniao = px.bar(opiniao_counts, x=opiniao_counts.index, y=opiniao_counts, title="Contagem de Opiniões sobre a LITTERACI")
fig_opiniao.update_layout(xaxis_title="Opinião", yaxis_title="Contagem", xaxis_tickangle=-45)
st.plotly_chart(fig_opiniao)

# Atualizar dados
if st.button("Atualizar Dados"):
    df = load_data()
    st.experimental_rerun()