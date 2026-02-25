import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Sistema de Apoio à Decisão Clínica", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("modelo_obesidade.pkl")

model = load_model()

label_map = {
    'Insufficient_Weight': 'Baixo Peso',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I',
    'Obesity_Type_II': 'Obesidade Grau II',
    'Obesity_Type_III': 'Obesidade Grau III'
}

st.title("🏥 Sistema de Apoio à Decisão Clínica")
st.markdown("Sistema baseado em Machine Learning para classificação do nível de obesidade.")

st.sidebar.title("Informações do Sistema")
st.sidebar.markdown("""
**Modelo:** Random Forest (Scikit-learn)  
**Pipeline:** Pré-processamento + Classificador  
**Objetivo:** Apoio à decisão clínica  

Este sistema auxilia profissionais da saúde na classificação preditiva do nível de obesidade com base em variáveis clínicas e comportamentais.
""")

st.sidebar.markdown("---")
st.sidebar.caption("Projeto Acadêmico - Data Science aplicada à Saúde")

st.header("Perfil do Paciente")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gênero", ["Male", "Female"], format_func=lambda x: "Masculino" if x == "Male" else "Feminino")
        age = st.number_input("Idade", 1, 120, 25)
        height = st.number_input("Altura (m)", 1.0, 2.5, 1.75, step=0.01)
        weight = st.number_input("Peso (kg)", 10.0, 300.0, 70.0, step=0.1)
        family_history = st.selectbox("Histórico Familiar de Sobrepeso?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")

    with col2:
        favc = st.selectbox("Consome alimentos calóricos com frequência?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")
        fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1.0, 3.0, 2.0)
        ncp = st.slider("Número de refeições principais por dia", 1, 4, 3)
        caec = st.selectbox("Consome alimentos entre as refeições?", ["Sometimes", "Frequently", "Always", "no"],
                            format_func=lambda x: {"Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre", "no": "Não"}[x])
        smoke = st.selectbox("O paciente fuma?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")

    submitted = st.form_submit_button("Gerar Diagnóstico")

if submitted:
    input_data = pd.DataFrame([{
        'Gender': gender,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'family_history': family_history,
        'FAVC': favc,
        'FCVC': fcvc,
        'NCP': ncp,
        'CAEC': caec,
        'SMOKE': smoke,
        'CH2O': 2.0,
        'SCC': 'no',
        'FAF': 1.0,
        'TUE': 1.0,
        'CALC': 'Sometimes',
        'MTRANS': 'Public_Transportation'
    }])

    imc = weight / (height ** 2)

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    resultado_pt = label_map.get(prediction, prediction)
    confianca = max(probabilities) * 100

    st.subheader(f"Resultado do Diagnóstico: **{resultado_pt}**")
    st.metric("Confiança do Modelo", f"{confianca:.2f}%")
    st.info(f"IMC Calculado: {imc:.2f}")

    prob_df = pd.DataFrame({
        "Categoria": model.classes_,
        "Probabilidade": probabilities
    }).sort_values(by="Probabilidade", ascending=False)

    st.bar_chart(prob_df.set_index("Categoria"))
