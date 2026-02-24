import streamlit as st
import pandas as pd
import joblib

# Carregamento do pipeline completo e mapeamento de tradução
model = joblib.load('modelo_obesidade.pkl')

# Dicionário para traduzir o resultado final para o médico
label_map = {
    'Insufficient_Weight': 'Baixo Peso',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I',
    'Obesity_Type_II': 'Obesidade Grau II',
    'Obesity_Type_III': 'Obesidade Grau III'
}

st.set_page_config(page_title="Predição de Obesidade", layout="centered")

st.title("🏥 Sistema de Apoio à Decisão Clínica")
st.markdown("Insira os dados do paciente para obter o diagnóstico preditivo.")

st.sidebar.header("Perfil do Paciente")

# Formulário de entrada de dados
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gênero", options=["Male", "Female"], format_func=lambda x: "Masculino" if x == "Male" else "Feminino")
        age = st.number_input("Idade", min_value=1, max_value=120, value=25)
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.75, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
        family_history = st.selectbox("Histórico Familiar de Sobrepeso?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")

    with col2:
        favc = st.selectbox("Consome alimentos calóricos com frequência?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")
        fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1.0, 3.0, 2.0)
        ncp = st.slider("Número de refeições principais por dia", 1, 4, 3)
        caec = st.selectbox("Consome alimentos entre as refeições?", options=["Sometimes", "Frequently", "Always", "no"], format_func=lambda x: {"Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre", "no": "Não"}[x])
        smoke = st.selectbox("O paciente fuma?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")

    st.markdown("---")
    submitted = st.form_submit_button("Gerar Diagnóstico")

if submitted:
    # Organização dos dados exatamente como o modelo espera (Nomes em Inglês)
    input_data = pd.DataFrame([{
        'Gender': gender, 'Age': age, 'Height': height, 'Weight': weight,
        'family_history': family_history, 'FAVC': favc, 'FCVC': fcvc,
        'NCP': ncp, 'CAEC': caec, 'SMOKE': smoke,
        'CH2O': 2.0, 'SCC': 'no', 'FAF': 1.0, 'TUE': 1.0, # Valores médios para campos não incluídos no form simplificado
        'CALC': 'Sometimes', 'MTRANS': 'Public_Transportation'
    }])

    # Predição e tradução do resultado
    prediction = model.predict(input_data)[0]
    resultado_pt = label_map.get(prediction, prediction)

    st.subheader(f"Resultado do Diagnóstico: **{resultado_pt}**")
