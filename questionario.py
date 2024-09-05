import streamlit as st

# Título
st.title("Questionário de Validação de Ideação")

# Introdução
st.markdown("Por favor, responda às perguntas abaixo para nos ajudar a validar nossa ideação.")

# Pergunta 1: O que você acha da ideia proposta?
op1 = st.radio("O que você acha da nossa ideia?", ("Muito boa", "Boa", "Regular", "Ruim"))

# Pergunta 2: Você usaria o produto/serviço?
op2 = st.selectbox("Você usaria esse produto/serviço?", ("Sim", "Não"))

# Pergunta 3: Qual recurso você acha mais importante?
op3 = st.multiselect(
    "Qual recurso você acha mais importante no produto?",
    ["Facilidade de uso", "Preço", "Acessibilidade", "Design", "Suporte ao cliente"]
)

# Pergunta 4: Comentários adicionais
op4 = st.text_area("Comentários adicionais")

# Botão de submissão
if st.button("Enviar respostas"):
    st.success("Obrigado por suas respostas!")
    st.write("Resumo das respostas:")
    st.write(f"Opinião sobre a ideia: {op1}")
    st.write(f"Usaria o produto: {op2}")
    st.write(f"Recursos mais importantes: {', '.join(op3)}")
    st.write(f"Comentários adicionais: {op4}")
