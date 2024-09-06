# Lib Session

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import uuid
from datetime import datetime

# Database do Google Sheets - Configuração
# Definir o escopo
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carregar as credenciais do secret
creds_dict = st.secrets["gcp_service_account"]

# Autenticar usando as credenciais do secret em formato de dicionário
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Autenticar no Google Sheets
client = gspread.authorize(creds)
sheet = client.open("LITTERACI_DB").sheet1

# Captura de dados de seção do usuário
# Função para gerar um UUID único para identificar a sessão do respondente
def generate_session_id():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]

# Gerar o timestamp e a ID de sessão
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
session_id = generate_session_id()

######## O Formulário comeca aqui ########
# Título do formulário
st.title("Pesquisa de Validação - LITTERACI")

# Estilo do formulário
st.markdown(
    """
    <style>
    /* Forçar modo claro */
    :root {
        --background-color: #F9F9F9;
        --text-color: #000000;
        --button-background-color: #2E86C1;
        --button-text-color: #FFFFFF;
        --input-background-color: #FFFFFF;
    }

    /* Aplicar cores ao fundo e texto */
    body {
        background-color: #A42593 !important;
        color: var(--text-color) !important;
    }

    /* Estilizar botões */
    .css-1d391kg {
        background-color: var(--button-background-color) !important;
        color: var(--button-text-color) !important;
    }
    .css-1d391kg:hover {
        background-color: #1F618D !important;
    }

    /* Estilizar caixas de texto e seletores */
    .stTextInput input {
        background-color: var(--input-background-color) !important;
    }
    .stSelectbox select {
        background-color: var(--input-background-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Perguntas do formulário
# Pergunta 1: Tipo de Unidade de Informação
tipo_ui = st.selectbox("Tipo de Unidade de Informação (UI) na qual trabalha atualmente, ou que atuou nos últimos 5 anos:", 
                       ["Arquivo (setor público)", "Arquivo (setor privado)", "Biblioteca (setor público)", 
                        "Biblioteca (setor privado)", "Museu (setor público)", "Museu (setor privado)", 
                        "Outro tipo de Unidade de Informação"])

# Pergunta 2 em diante: Escala de 0 a 10
escalas = [
    "O comportamento do(s) usuário(s) que minha Unidade de Informação atende tem mudado nos últimos 5 anos",
    "O número de usuários que utiliza minha Unidade de Informação tem aumentado nos últimos 5 anos",
    "Minha Unidade de Informação consegue atender plenamente qualquer demanda informacional do meu usuário",
    "Minha base de dados/catálogo consegue recuperar de maneira satisfatória qualquer dado ou informação demandado pelo usuário",
    "Minha Unidade de Informação possui sistemas de informação que conseguem atender/recuperar/responder qualquer demanda do usuário",
    "Minha Unidade de Informação possui bases de dados interligadas com outras UIs",
    "Minha Unidade de Informação possui serviço de curadoria de dados e de conteúdo para o usuário",
    "Minha Unidade de Informação trabalha com soluções baseadas em Inteligência Artificial (IA)",
    "Minha Unidade de Informação está mudando seus processos, produtos e/ou serviços por causa do novo contexto digital",
    "Minha Unidade de Informação analisa o comportamento de busca dos usuários para criar novos produtos e serviços baseados nas suas necessidades",
    "Minha Unidade de Informação trabalha com indicadores sobre a satisfação do usuário",
    "Minha Unidade de Informação é um lugar onde meu usuário gosta de estar presente fisicamente",
    "Minha Unidade de Informação é a primeira opção para meu usuário quando ele busca por informação",
    "Minha Unidade de Informação está totalmente adaptada aos novos comportamentos dos usuários",
    "Minha Unidade de Informação precisará mudar seu modo de atuar para se manter útil e ativa no futuro",
    "Se a minha Unidade de Informação não mudar sua forma de atender o usuário, ela não irá sobreviver no futuro",
    "Até 2030, o modelo de funcionamento da minha Unidade de Informação será totalmente diferente do atual"
]

# Loop para gerar perguntas de escala 0-10
respostas_escala = {}
for pergunta in escalas:
    respostas_escala[pergunta] = st.slider(pergunta, 0, 10, 5)

# Pergunta: Opinião sobre a LITTERACI
opcoes_litteraci = st.multiselect(
    "A partir dessa breve descrição da LITTERACI, gostaria de saber qual(is) a(s) sua(s) opinião(ões)?",
    ["A LITTERACI ajudaria minha Unidade de Informação a se manter atual e ativa",
     "A minha Unidade de Informação precisa dessa solução para aprimorar a sua forma de atendimento ao usuário",
     "Eu e/ou a minha Unidade de Informação estaria disposto(a) a conhecer com mais detalhes a LITTERACI",
     "Eu e/ou a minha Unidade de Informação estaria disposto(s) a adquirir a solução LITTERACI",
     "Eu e/ou minha Unidade de Informação não tenho interesse em conhecer e/ou adquirir essa solução"]
)

# Pergunta: Feedback final e contato
feedback = st.text_area("Obrigado por responder a esta pesquisa! Caso queira receber um retorno sobre suas respostas, basta digitar abaixo seu nome e email. Entraremos em contato!")

# Fim do formulário

# Submissão do formulário
# Botão de envio
if st.button("Enviar respostas"):

    respostas_completas = [timestamp, session_id, tipo_ui] + respostas_escala + [", ".join(opcoes_litteraci), feedback]
    
    # Gravar no Google Sheets
    sheet.append_row(respostas_completas)
    
    st.success("Obrigado por participar da pesquisa!")
    st.write("Suas respostas foram enviadas com sucesso. A LITTERACI agradece a sua colaboração!")