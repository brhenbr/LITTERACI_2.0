import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud

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
    </style>
    """,
    unsafe_allow_html=True
)

# Título do dashboard
st.title("Análise das Respostas da Pesquisa LITTERACI")

# Introdução
st.write("Bem-vindo ao dashboard de análise das respostas da pesquisa LITTERACI! Aqui, você encontrará insights valiosos sobre a situação atual e futura das Unidades de Informação (UIs), bem como as opiniões dos participantes sobre a solução inovadora LITTERACI.")

# Visão Geral
st.header("Visão Geral")
total_respostas = len(df)
st.subheader(f"Total de respostas: {total_respostas}")

# Tipos de UI
st.subheader("Tipos de Unidades de Informação")
tipo_ui_counts = df["Tipo de UI"].value_counts()
fig_tipo_ui = px.pie(tipo_ui_counts, values=tipo_ui_counts, names=tipo_ui_counts.index, title="Distribuição dos Tipos de UI")
fig_tipo_ui.update_layout(title_font=dict(size=20))
st.plotly_chart(fig_tipo_ui)

st.write("A pesquisa abrangeu diversos tipos de Unidades de Informação, proporcionando uma visão ampla e representativa do cenário atual.")

# Situação Atual
st.header("Situação Atual das Unidades de Informação")
st.write("Vamos explorar as respostas dos participantes sobre a situação atual de suas UIs.")

situacao_atual_media = situacao_atual_data.mean().round(2)
fig_atual = px.bar(situacao_atual_media, x=situacao_atual_media.index, y=situacao_atual_media.values, 
                   labels={"x": "Pergunta", "y": "Média"}, title="Média das Respostas - Situação Atual")
fig_atual.update_layout(title_font=dict(size=20), xaxis_title="Pergunta", yaxis_title="Média", xaxis_tickangle=-45)
st.plotly_chart(fig_atual)

st.write("As respostas indicam que as UIs enfrentam desafios significativos na adaptação ao novo contexto digital e na satisfação das necessidades dos usuários.")

# Situação Futura
st.header("Perspectivas para o Futuro das Unidades de Informação")
st.write("Agora, vamos analisar as perspectivas dos participantes sobre o futuro de suas UIs.")

situacao_futura_media = situacao_futura_data.mean().round(2)
fig_futura = px.bar(situacao_futura_media, x=situacao_futura_media.index, y=situacao_futura_media.values,
                    labels={"x": "Pergunta", "y": "Média"}, title="Média das Respostas - Situação Futura")
fig_futura.update_layout(title_font=dict(size=20), xaxis_title="Pergunta", yaxis_title="Média", xaxis_tickangle=-45)
st.plotly_chart(fig_futura)

st.write("Os resultados mostram que os participantes reconhecem a necessidade de mudança e adaptação das UIs para se manterem relevantes e atender às demandas futuras dos usuários.")

# Opiniões sobre a LITTERACI
st.header("Opiniões sobre a Solução LITTERACI")
st.write("Por fim, vamos explorar as opiniões dos participantes sobre a solução inovadora LITTERACI.")

opinioes_text = " ".join(df["Opinioes UI"].str.cat(sep=" "))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(opinioes_text)

fig_opiniao, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
ax.set_title("Nuvem de Palavras - Opiniões sobre a LITTERACI", fontsize=20)
st.pyplot(fig_opiniao)

st.write("A nuvem de palavras destaca os termos mais frequentes nas opiniões dos participantes, indicando um interesse significativo em conhecer e adotar a solução LITTERACI para aprimorar os serviços das UIs.")

# Conclusão
st.header("Conclusão")
st.write("A análise das respostas da pesquisa LITTERACI revelou insights valiosos sobre a situação atual e futura das Unidades de Informação. Os resultados apontam para a necessidade de adaptação e inovação das UIs para atender às demandas do novo contexto digital e satisfazer as necessidades dos usuários.")
st.write("A solução LITTERACI surge como uma proposta promissora para auxiliar as UIs nessa transformação, oferecendo recursos avançados de integração, curadoria e inteligência artificial. O interesse demonstrado pelos participantes reforça o potencial da LITTERACI em impulsionar a evolução das UIs.")
st.write("Esperamos que este dashboard tenha proporcionado uma visão clara e envolvente dos resultados da pesquisa. Agradecemos a participação de todos e convidamos vocês a explorar a solução LITTERACI para transformar suas Unidades de Informação.")

# Rodapé
st.markdown("---")
st.write("Dashboard desenvolvido por [Seu Nome] | Powered by Streamlit")

# Logo
logo = Image.open('images/logo.png')
st.image(logo, width=150, use_column_width=True)