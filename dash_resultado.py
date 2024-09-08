import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import plotly.figure_factory as ff
from PIL import Image
import io
import base64

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
    scale_data.columns = scale_data.columns.astype(int) + 1
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
        --font-size-title: 28px;
        --font-size-subtitle: 20px;
    }
    /* Resto do CSS... */
    .pergunta {
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
    }
    .opiniao-table {
        background-color: #F2F2F2;
        border-radius: 5px;
        padding: 10px;
    }
    .opiniao-table td {
        padding: 8px;
    }
    .opiniao-table tr:nth-child(even) {
        background-color: #E6E6E6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo
col1, col2 = st.columns([1, 4])
with col1:
    logo = Image.open('images/logo.png')
    st.image(logo, width=100)
    st.empty()  # Espaço vazio para manter o logo fixo

# Título do dashboard
st.title("Análise das Respostas da Pesquisa LITTERACI")

# Introdução
st.write("Bem-vindo ao dashboard de análise das respostas da pesquisa LITTERACI! Aqui, você encontrará insights valiosos sobre a situação atual e futura das Unidades de Informação (UIs), bem como as opiniões dos participantes sobre a solução inovadora LITTERACI.")

# Filtro por tipo de UI
st.sidebar.title("Filtro")
tipo_ui_options = ["Todas"] + list(df["Tipo de UI"].unique())
selected_ui_types = st.sidebar.multiselect("Selecione o tipo de UI", options=tipo_ui_options, default=["Todas"])

# Aplicar filtro
if "Todas" in selected_ui_types:
    filtered_df = df
    filtered_situacao_atual = situacao_atual_data
    filtered_situacao_futura = situacao_futura_data
else:
    filtered_df = df[df["Tipo de UI"].isin(selected_ui_types)]
    filtered_situacao_atual = situacao_atual_data[df["Tipo de UI"].isin(selected_ui_types)]
    filtered_situacao_futura = situacao_futura_data[df["Tipo de UI"].isin(selected_ui_types)]

# Visão Geral
st.header("Visão Geral")
total_respostas = len(filtered_df)
st.subheader(f"Total de respostas: {total_respostas}")

# Tipos de UI
st.subheader("Tipos de Unidades de Informação")
tipo_ui_counts = filtered_df["Tipo de UI"].value_counts()
fig_tipo_ui = px.pie(tipo_ui_counts, values=tipo_ui_counts, names=tipo_ui_counts.index, title="Distribuição dos Tipos de UI")
fig_tipo_ui.update_layout(title_font=dict(size=20))
st.plotly_chart(fig_tipo_ui, use_container_width=True)

# Situação Atual
st.header("Situação Atual das Unidades de Informação")

situacao_atual_perguntas = [
    "O comportamento do(s) usuário(s) que minha Unidade de Informação atende tem mudado nos últimos 5 anos",
    "O número de usuários que utiliza minha Unidade de Informação (espaço físico, site, produtos, serviços, etc.) tem aumentado nos últimos 5 anos",
    "Minha Unidade de Informação consegue atender plenamente qualquer demanda informacional do meu usuário",
    "Minha base de dados/catálogo consegue recuperar de maneira satisfatória qualquer dado ou informação demandado pelo usuário",
    "Minha Unidade de Informação possui sistemas de informação que conseguem atender/recuperar/responder qualquer demanda do usuário",
    "Minha Unidade de Informação possui bases de dados interligadas com outras UIs",
    "Minha Unidade de Informação possui serviço de curadoria de dados e de conteúdo para o usuário",
    "Minha Unidade de Informação trabalha com soluções (produtos e/ou serviços) baseadas em Inteligência Artificial (IA)",
    "Minha Unidade de Informação está mudando/mudou seus processos, produtos e/ou serviços por causa do novo contexto digital",
    "Minha Unidade de Informação analisa o comportamento de busca dos usuários para criar novos produtos e serviços baseados nas suas necessidades",
    "Minha Unidade de Informação trabalha com indicadores sobre a satisfação do usuário, a retenção do usuário e a recomendação do usuário a outras pessoas",
    "Minha Unidade de Informação é um lugar onde meu usuário gosta de estar presente fisicamente",
    "Minha Unidade de Informação é a primeira opção para meu usuário quando ele busca por informação"
]

col1, col2, col3 = st.columns(3)
for i, pergunta in enumerate(situacao_atual_perguntas, start=1):
    if i % 3 == 1:
        with col1:
            if len(filtered_situacao_atual[i]) > 0:
                fig = ff.create_distplot([filtered_situacao_atual[i]], [pergunta], bin_size=1, show_rug=False)
                fig.update_layout(xaxis_title="Nota", yaxis_title="Frequência")
                st.plotly_chart(fig)
            else:
                st.warning(f"Não há dados suficientes para exibir o gráfico da Pergunta {i}.")
            st.markdown(f'<div class="pergunta" title="{pergunta}">Pergunta {i}</div>', unsafe_allow_html=True)
    elif i % 3 == 2:
        with col2:
            if len(filtered_situacao_atual[i]) > 0:
                fig = ff.create_distplot([filtered_situacao_atual[i]], [pergunta], bin_size=1, show_rug=False)
                fig.update_layout(xaxis_title="Nota", yaxis_title="Frequência")
                st.plotly_chart(fig)
            else:
                st.warning(f"Não há dados suficientes para exibir o gráfico da Pergunta {i}.")
            st.markdown(f'<div class="pergunta" title="{pergunta}">Pergunta {i}</div>', unsafe_allow_html=True)
    else:
        with col3:
            if len(filtered_situacao_atual[i]) > 0:
                fig = ff.create_distplot([filtered_situacao_atual[i]], [pergunta], bin_size=1, show_rug=False)
                fig.update_layout(xaxis_title="Nota", yaxis_title="Frequência")
                st.plotly_chart(fig)
            else:
                st.warning(f"Não há dados suficientes para exibir o gráfico da Pergunta {i}.")
            st.markdown(f'<div class="pergunta" title="{pergunta}">Pergunta {i}</div>', unsafe_allow_html=True)

# Situação Futura
st.header("Perspectivas para o Futuro das Unidades de Informação")

situacao_futura_perguntas = [
    "Minha Unidade de Informação está totalmente adaptada aos novos comportamentos dos usuários (considerando o contexto digital)",
    "Minha Unidade de Informação precisará mudar seu modo de atuar para se manter útil e ativa no futuro",
    "Se a minha Unidade de Informação não mudar sua forma de atender o usuário, ela não irá sobreviver no futuro",
    "Até 2030, o modelo de funcionamento da minha Unidade de Informação será totalmente diferente do atual"
]

col1, col2 = st.columns(2)
for i, pergunta in enumerate(situacao_futura_perguntas, start=1):
    if i % 2 == 1:
        with col1:
            if len(filtered_situacao_futura[i]) > 0:
                fig = ff.create_distplot([filtered_situacao_futura[i]], [pergunta], bin_size=1, show_rug=False)
                fig.update_layout(xaxis_title="Nota", yaxis_title="Frequência")
                st.plotly_chart(fig)
            else:
                st.warning(f"Não há dados suficientes para exibir o gráfico da Pergunta {i}.")
            st.markdown(f'<div class="pergunta" title="{pergunta}">Pergunta {i}</div>', unsafe_allow_html=True)
    else:
        with col2:
            if len(filtered_situacao_futura[i]) > 0:
                fig = ff.create_distplot([filtered_situacao_futura[i]], [pergunta], bin_size=1, show_rug=False)
                fig.update_layout(xaxis_title="Nota", yaxis_title="Frequência")
                st.plotly_chart(fig)
            else:
                st.warning(f"Não há dados suficientes para exibir o gráfico da Pergunta {i}.")
            st.markdown(f'<div class="pergunta" title="{pergunta}">Pergunta {i}</div>', unsafe_allow_html=True)

# Opiniões sobre a LITTERACI
st.header("Opiniões sobre a Solução LITTERACI")

opcoes_litteraci = filtered_df["Opinioes UI"].str.split(";", expand=True).stack()
opcoes_litteraci = opcoes_litteraci[opcoes_litteraci != ""]
opiniao_counts = opcoes_litteraci.value_counts()

opiniao_df = pd.DataFrame({"Opinião": opiniao_counts.index, "Contagem": opiniao_counts.values})
st.table(opiniao_df)

# Download dos dados de contato
st.header("Dados de Contato")
st.write("Clique no botão abaixo para baixar os dados de contato dos participantes em um arquivo CSV.")

def download_csv(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href

contato_df = filtered_df[["Dados Contato"]]
csv_download_link = download_csv(contato_df, "dados_contato.csv")
st.download_button("Download CSV", csv_download_link, "dados_contato.csv")

# Conclusão
st.header("Conclusão")
st.write("A análise das respostas da pesquisa LITTERACI revelou insights valiosos sobre a situação atual e futura das Unidades de Informação. Os resultados apontam para a necessidade de adaptação e inovação das UIs para atender às demandas do novo contexto digital e satisfazer as necessidades dos usuários.")
st.write("A solução LITTERACI surge como uma proposta promissora para auxiliar as UIs nessa transformação, oferecendo recursos avançados de integração, curadoria e inteligência artificial. O interesse demonstrado pelos participantes reforça o potencial da LITTERACI em impulsionar a evolução das UIs.")
st.write("Esperamos que este dashboard tenha proporcionado uma visão clara e envolvente dos resultados da pesquisa. Agradecemos a participação de todos e convidamos vocês a explorar a solução LITTERACI para transformar suas Unidades de Informação.")

# Rodapé
st.markdown("---")
st.write("Dashboard desenvolvido por LITTERACI | Powered by Streamlit")