import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurações para acesso ao Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("litteraci-ee78c6f34fef.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Nome_da_sua_planilha").sheet1

# Título
st.title("Questionário de Validação de Ideação")

# Introdução
st.markdown("Por favor, responda às perguntas abaixo para nos ajudar a validar nossa ideação.")

# Perguntas
op1 = st.radio("O que você acha da nossa ideia?", ("Muito boa", "Boa", "Regular", "Ruim"))
op2 = st.selectbox("Você usaria esse produto/serviço?", ("Sim", "Não"))
op3 = st.multiselect("Qual recurso você acha mais importante no produto?", ["Facilidade de uso", "Preço", "Acessibilidade", "Design", "Suporte ao cliente"])
op4 = st.text_area("Comentários adicionais")

# Botão de submissão
if st.button("Enviar respostas"):
    st.success("Obrigado por suas respostas!")
    st.write("Resumo das respostas:")
    st.write(f"Opinião sobre a ideia: {op1}")
    st.write(f"Usaria o produto: {op2}")
    st.write(f"Recursos mais importantes: {', '.join(op3)}")
    st.write(f"Comentários adicionais: {op4}")

    # Adiciona as respostas à planilha
    sheet.append_row([op1, op2, ', '.join(op3), op4])
