# Lib Session

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import uuid
from datetime import datetime
from PIL import Image

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
st.markdown("<h1>Pesquisa de Validação - LITTERACI</h1>",unsafe_allow_html=True)

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
        --slider-color: #A42593; /* Cor do slider */
        --question-font-size: 16px; /* Tamanho da fonte das perguntas */        
    }

    /* Aplicar cores ao fundo e texto */
    body {
        background-color: var(--background-color) !important;
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
    /* Aumentar o tamanho da fonte das perguntas */
    .css-fonte {
        font-size: var(--question-font-size) !important;
        font-weight: bold;
    }

    /* Estilizar o slider */
    .stSlider {
        color: var(--slider-color) !important;
    }

    /* Estilizar textos para separação de seções */
    .section-title {
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Estilizar a logo marca ao final da página */
    .logo {
        text-align: center;
        margin-top: 40px;
    }
    .logo img {
        width: 150px;
        height: auto;
    }    
    </style>
    """,
    unsafe_allow_html=True
)

# Adicionar separação e textos para seções
st.markdown("<div class='section-title'> Olá! Obrigado por aceitar participar desta pesquisa sobre Unidades de Informação (Arquivos, Bibliotecas, Museus)!<br>Responda as perguntas a seguir com base na Unidade de Informação (UI) na qual você trabalha atualmente, ou que atuou nos últimos 5 anos.<br></div>", unsafe_allow_html=True)

titulo = st.markdown("<div class='css-fonte'><br>Tipo de Unidade de Informação (UI) na qual trabalha atualmente, ou que atuou nos últimos 5 anos:</div>", unsafe_allow_html=True)

# Perguntas do formulário
# Pergunta 1: Tipo de Unidade de Informação
tipo_ui = st.selectbox("", 
                       ["Arquivo (setor público)", "Arquivo (setor privado)", "Biblioteca (setor público)", 
                        "Biblioteca (setor privado)", "Museu (setor público)", "Museu (setor privado)", 
                        "Outro tipo de Unidade de Informação"])

# Pergunta em Escala de 0 a 10 - Parte 1
st.markdown("<h2>Situação atual (presente) da minha Unidade de Informação (UI)</h2>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'> Gostaria que você desse uma nota, de 0 a 10, considerando a escala de concordância/discordância abaixo, sobre algumas afirmativas relacionadas à situação atual de sua Unidade de Informação (UI) 0. Discordo totalmente (DT) -   1   -   2   -   3   -   4   -   5   -   6   -  7   -  8   -   9   -   10. Concordo totalmente (CT).</div>", unsafe_allow_html=True)

escalas_1 = [
    st.markdown("<div class='css-fonte'><br>O comportamento do(s) usuário(s) que minha Unidade de Informação atende tem mudado nos últimos 5 anos</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>O número de usuários que utiliza minha Unidade de Informação (espaço físico, site, produtos, serviços, etc.) tem aumentado nos últimos 5 anos</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>Minha Unidade de Informação consegue atender plenamente qualquer demanda informacional do meu usuário</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>Minha base de dados/catálogo consegue recuperar de maneira satisfatória qualquer dado ou informação demandado pelo usuário</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>Minha Unidade de Informação possui sistemas de informação que conseguem atender/recuperar/responder qualquer demanda do usuário</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>Minha Unidade de Informação possui bases de dados interligadas com outras UIs</div>", unsafe_allow_html=True),
    st.markdown("<div class='css-fonte'><br>Minha Uindade de Informação possui serviço de curadoria de dados e de conteúdo para o usuário</div>", unsafe_allow_html=True),
    "Minha Unidade de Informação trabalha com soluções (produtos e/ou serviços) baseadas em Inteligência Artificial (IA)",
    "Minha Unidade de Informação está mudando/mudou seus processos, produtos e/ou serviços por causa do novo contexto digital",
    "Minha Unidade de Informação analisa o comportamento de busca dos usuários para criar novos produtos e serviços baseados nas suas necessidades",
    "Minha Unidade de Informação trabalha com indicadores sobre a satisfação do usuário, a retenção do usuário e a recomendação do usuário a outras pessoas",
    "Minha Unidade de Informação é um lugar onde meu usuário gosta de estar presente fisicamente",
    "Minha Unidade de Informação é a primeira opção para meu usuário quando ele busca por informação",
]

# Loop para gerar perguntas de escala 0-10
respostas_escala_1 = {}
for pergunta in escalas_1:
    respostas_escala_1[pergunta] = st.slider(pergunta, 0, 10, 2)


# Pergunta em Escala de 0 a 10 - Parte 2
st.markdown("<h2>Situação futura da minha Unidade de Informação (UI)</h2>",unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'> Agora, gostaria que você desse uma nota, de 0 a 10, considerando a escala de concordância/discordância abaixo, sobre algumas afirmativas relacionadas à situação futura de sua Unidade de Informação (UI), e considerando os próximos 5 anos (até 2030). 0. Discordo totalmente (DT) -   1   -   2   -   3   -   4   -   5   -   6   -  7   -  8   -   9   -   10. Concordo totalmente (CT)</div>", unsafe_allow_html=True)

escalas_2 = [
    "Minha Unidade de Informação está totalmente adaptada aos novos comportamentos dos usuários (considerando o contexto digital)",
    "Minha Unidade de Informação precisará mudar seu modo de atuar para se manter útil e ativa no futuro ",
    "Se a minha Unidade de Informação não mudar sua forma de atender o usuário, ela não irá sobreviver no futuro ",
    "Até 2030, o modelo de funcionamento da minha Unidade de Informação será totalmente diferente do atual",
   
]

# Loop para gerar perguntas de escala 0-10
respostas_escala_2 = {}
for pergunta in escalas_2:
    respostas_escala_2[pergunta] = st.slider(pergunta, 0, 10, 2)    


# Pergunta: Opinião sobre a LITTERACI

var_texto = """<div class='section-subtitle'>Para encerrarmos nossa entrevista, quero apresentar-lhe uma breve descrição de uma potencial solução inovadora para Unidades 
de Informação em geral, denominada LITTERACI: <br> A LITTERACI é uma solução pioneira para Unidades de Informação, plataforma que integra diversos 
tipos de fontes de informação (como catálogos, bases de dados, bibliotecas digitais e repositórios) em uma única interface, 
tecnologias de Customer Relationship Management (CRM) e Business Intelligence (BI) para aprendizado contínuo e enriquecimento 
constante do acervo, analytics para monitorar e aprimorar continuamente a precisão e a relevância das buscas, e curadoria personalizada no 
atendimento de qualquer demanda informacional. Ao integrar a linguagem natural do usuário e a curadoria especializada aos metadados tradicionais, 
a LITTERACI proporciona uma recuperação mais precisa e relevante dos recursos informacionais, promovendo uma interação mais eficiente e 
personalizada dos conteúdos disponíveis.</div>"""

st.markdown("<h2>Proposta de Solução Inovadora</h2>",unsafe_allow_html=True)
st.markdown(var_texto, unsafe_allow_html=True)

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

    respostas_completas = [timestamp, session_id, tipo_ui] + respostas_escala_1 + respostas_escala_1 + [", ".join(opcoes_litteraci), feedback]
    
    # Gravar no Google Sheets
    sheet.append_row(respostas_completas)
    
    st.success("Obrigado por participar da pesquisa!")
    st.write("Suas respostas foram enviadas com sucesso. A LITTERACI agradece a sua colaboração!")

logo = Image.open('images/logo.png')
st.image(logo, use_column_width=True)