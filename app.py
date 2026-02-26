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
st.markdown("Sistema baseado em Machine Learning para suporte à classificação clínica do nível de obesidade.")

st.sidebar.title("Informações do Sistema")
st.sidebar.markdown("""
**Modelo:** Random Forest (Scikit-learn)  
**Pipeline:** Pré-processamento + Classificador  
**Objetivo:** Apoiar equipes médicas na avaliação do estado nutricional  

Este sistema fornece suporte à decisão com base em variáveis clínicas e comportamentais.
""")

st.sidebar.markdown("---")
st.sidebar.caption("Projeto Acadêmico - Data Science aplicada à Saúde")

st.header("Perfil do Paciente")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gênero", ["Male", "Female"],
                              format_func=lambda x: "Masculino" if x == "Male" else "Feminino")
        age = st.number_input("Idade", 1, 120, 25)
        height = st.number_input("Altura (m)", 1.0, 2.5, 1.75, step=0.01)
        weight = st.number_input("Peso (kg)", 10.0, 300.0, 70.0, step=0.1)
        family_history = st.selectbox("Histórico Familiar de Sobrepeso?",
                                      ["yes", "no"],
                                      format_func=lambda x: "Sim" if x == "yes" else "Não")

    with col2:
        favc = st.selectbox("Consome alimentos calóricos com frequência?",
                            ["yes", "no"],
                            format_func=lambda x: "Sim" if x == "yes" else "Não")
        fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1.0, 3.0, 2.0)
        ncp = st.slider("Número de refeições principais por dia", 1, 4, 3)
        caec = st.selectbox("Consome alimentos entre as refeições?",
                            ["Sometimes", "Frequently", "Always", "no"],
                            format_func=lambda x: {
                                "Sometimes": "Às vezes",
                                "Frequently": "Frequentemente",
                                "Always": "Sempre",
                                "no": "Não"}[x])
        smoke = st.selectbox("O paciente fuma?",
                             ["yes", "no"],
                             format_func=lambda x: "Sim" if x == "yes" else "Não")

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

    st.subheader(f"Resultado do Diagnóstico: **{resultado_pt}**")
    st.info(f"IMC Calculado: {imc:.2f}")

    # Classificação IMC
    if imc < 18.5:
        classificacao_imc = "Baixo Peso"
    elif 18.5 <= imc < 25:
        classificacao_imc = "Peso Normal"
    elif 25 <= imc < 30:
        classificacao_imc = "Sobrepeso"
    elif 30 <= imc < 35:
        classificacao_imc = "Obesidade Grau I"
    elif 35 <= imc < 40:
        classificacao_imc = "Obesidade Grau II"
    else:
        classificacao_imc = "Obesidade Grau III"

    st.caption(f"Classificação pelo IMC: {classificacao_imc}")

    # Distribuição de probabilidades
    prob_df = pd.DataFrame({
        "Categoria Clínica": [label_map.get(c, c) for c in model.classes_],
        "Probabilidade (%)": probabilities * 100
    }).sort_values(by="Probabilidade (%)", ascending=False)

    st.markdown("### Distribuição da Classificação")
    st.bar_chart(prob_df.set_index("Categoria Clínica"))

    # Interpretação Clínica
    st.markdown("### Interpretação Clínica")

    interpretacoes = {
        "Baixo Peso": "Recomenda-se investigação nutricional detalhada.",
        "Peso Normal": "Manutenção de hábitos saudáveis e acompanhamento preventivo.",
        "Sobrepeso Nível I": "Intervenção nutricional e incentivo à atividade física.",
        "Sobrepeso Nível II": "Avaliação metabólica e acompanhamento clínico.",
        "Obesidade Grau I": "Risco aumentado para comorbidades. Monitoramento clínico recomendado.",
        "Obesidade Grau II": "Alto risco metabólico. Indica-se acompanhamento multiprofissional.",
        "Obesidade Grau III": "Obesidade grave associada a elevado risco cardiovascular."
    }

    st.write(interpretacoes.get(resultado_pt, ""))

    # Diretrizes
    st.markdown("### Diretrizes Clínicas Sugeridas")

    diretrizes = {
        "Baixo Peso": [
            "Avaliação nutricional completa",
            "Monitoramento clínico periódico"
        ],
        "Peso Normal": [
            "Manutenção de dieta equilibrada",
            "Atividade física regular"
        ],
        "Sobrepeso Nível I": [
            "Encaminhamento para nutricionista",
            "Plano estruturado de atividade física"
        ],
        "Sobrepeso Nível II": [
            "Avaliação cardiometabólica",
            "Intervenção comportamental"
        ],
        "Obesidade Grau I": [
            "Acompanhamento multiprofissional",
            "Investigação de comorbidades"
        ],
        "Obesidade Grau II": [
            "Encaminhamento para endocrinologista",
            "Considerar farmacoterapia conforme avaliação médica"
        ],
        "Obesidade Grau III": [
            "Encaminhamento para equipe multidisciplinar",
            "Avaliação psicológica",
            "Avaliação para elegibilidade de cirurgia bariátrica"
        ]
    }

    for item in diretrizes.get(resultado_pt, []):
        st.write(f"- {item}")

    # Alerta adicional para possível elegibilidade bariátrica baseada em IMC
    if imc >= 40:
        st.warning("IMC ≥ 40 kg/m²: Pode haver indicação para avaliação de elegibilidade para cirurgia bariátrica conforme diretrizes clínicas.")
    elif imc >= 35:
        st.warning("IMC ≥ 35 kg/m²: Avaliar presença de comorbidades para possível elegibilidade cirúrgica.")
