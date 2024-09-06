import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Definir o escopo
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carregar as credenciais do secret
creds_dict = st.secrets["gcp_service_account"]

# Autenticar usando as credenciais do secret em formato de dicionário
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Autenticar no Google Sheets
client = gspread.authorize(creds)
sheet = client.open("LITTERACI_DB").sheet1

# Código do seu formulário
st.title("Questionário de Validação de Ideação")

op1 = st.radio("O que você acha da nossa ideia?", ("Muito boa", "Boa", "Regular", "Ruim"))
op2 = st.selectbox("Você usaria esse produto/serviço?", ("Sim", "Não"))
op3 = st.multiselect("Qual recurso você acha mais importante no produto?", ["Facilidade de uso", "Preço", "Acessibilidade", "Design", "Suporte ao cliente"])
op4 = st.text_area("Comentários adicionais")

# Botão de submissão
if st.button("Enviar respostas"):
    st.success("Obrigado por suas respostas!")
    st.write(f"Opinião sobre a ideia: {op1}")
    st.write(f"Usaria o produto: {op2}")
    st.write(f"Recursos mais importantes: {', '.join(op3)}")
    st.write(f"Comentários adicionais: {op4}")

    # Adiciona as respostas à planilha
    sheet.append_row([op1, op2, ', '.join(op3), op4])
