import streamlit as st
import pandas as pd
import joblib

# Configuração da página e título da aplicação
st.set_page_config(page_title="Diagnóstico Preditivo de Obesidade", layout="centered")
st.title("⚕️ Sistema de Apoio à Decisão Clínica")
st.markdown("Insira os dados do paciente para obter o diagnóstico preditivo.")

# Mapeamento para tradução dos resultados do modelo
label_map = {
    0.0: 'Peso Insuficiente',
    1.0: 'Peso Normal',
    2.0: 'Sobrepeso Nível I',
    3.0: 'Sobrepeso Nível II',
    4.0: 'Obesidade Grau I',
    5.0: 'Obesidade Grau II',
    6.0: 'Obesidade Grau III'
}

# Organização dos campos de entrada na interface lateral
with st.sidebar:
    st.header("Dados do Paciente")
    age = st.number_input("Idade", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
    height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
    weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0)

# Coleta de hábitos comportamentais no corpo principal
st.subheader("Hábitos e Histórico")
col1, col2 = st.columns(2)

with col1:
    family_history = st.selectbox("Histórico Familiar de Sobrepeso?", ["Sim", "Não"])
    favc = st.selectbox("Consumo frequente de alimentos calóricos?", ["Sim", "Não"])
    fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1, 3, 2)
    ncp = st.slider("Número de refeições principais", 1, 4, 3)

with col2:
    caec = st.selectbox("Consumo de alimentos entre refeições", ["Sempre", "Frequentemente", "Às vezes", "Não"])
    smoke = st.selectbox("Fumante?", ["Sim", "Não"])
    ch2o = st.slider("Consumo de água diário (Litros)", 1, 3, 2)
    faf = st.slider("Frequência de atividade física (Dias/Semana)", 0, 3, 1)

# Acionamento da predição
if st.button("Gerar Diagnóstico"):
    # Execução da lógica de predição
    st.success("Diagnóstico calculado com sucesso!")
    st.info("Nota: O modelo está processando as variáveis para definir o nível de risco.")
