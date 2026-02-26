import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Sistema de Apoio à Decisão Clínica",
    layout="centered",
    page_icon="🏥"
)

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

# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.title("📋 Informações do Sistema")

st.sidebar.markdown("""
**Modelo:** Random Forest (Scikit-learn)  
**Pipeline:** Pré-processamento + Classificador  
**Objetivo:** Apoio à decisão clínica  

Sistema de suporte à decisão baseado em Machine Learning
para classificação do nível de obesidade.
""")

st.sidebar.markdown("---")
st.sidebar.caption("Projeto Acadêmico – Data Science aplicada à Saúde")

# ----------------------------
# TÍTULO
# ----------------------------

st.title("🏥 Sistema de Apoio à Decisão Clínica")
st.markdown("Sistema baseado em Machine Learning para classificação do nível de obesidade.")

st.markdown("---")
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
                                "no": "Não"
                            }[x])
        smoke = st.selectbox("O paciente fuma?",
                             ["yes", "no"],
                             format_func=lambda x: "Sim" if x == "yes" else "Não")

    submitted = st.form_submit_button("Gerar Diagnóstico")

# ----------------------------
# RESULTADO
# ----------------------------

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

    prediction = model.predict(input_data)[0]
    resultado_pt = label_map.get(prediction, prediction)

    imc = weight / (height ** 2)

    st.markdown("---")
    st.subheader(f"📌 Resultado do Diagnóstico: {resultado_pt}")
    st.info(f"IMC Calculado: {imc:.2f}")

    # ----------------------------
    # INTERPRETAÇÃO COMPLETA
    # ----------------------------

    st.markdown("## 🩺 Interpretação Clínica")

    interpretacoes = {
        "Baixo Peso": "Estado nutricional abaixo da faixa adequada, podendo estar associado a risco nutricional e imunológico.",
        "Peso Normal": "Estado nutricional dentro da faixa considerada adequada, sem indicativos atuais de risco metabólico relacionado ao peso.",
        "Sobrepeso Nível I": "Excesso de peso inicial com potencial risco metabólico futuro, especialmente se associado a fatores comportamentais.",
        "Sobrepeso Nível II": "Excesso de peso significativo com risco metabólico aumentado e necessidade de intervenção estruturada.",
        "Obesidade Grau I": "Obesidade estabelecida com risco aumentado para doenças cardiovasculares e metabólicas.",
        "Obesidade Grau II": "Obesidade moderada a grave com risco elevado de complicações metabólicas e cardiovasculares.",
        "Obesidade Grau III": "Obesidade grave com risco significativo à saúde e alta probabilidade de complicações sistêmicas."
    }

    st.write(interpretacoes.get(resultado_pt, ""))

    # ----------------------------
    # DIRETRIZES COMPLETAS
    # ----------------------------

    st.markdown("## 📋 Diretrizes Clínicas Sugeridas")

    diretrizes = {
        "Baixo Peso": [
            "Avaliação nutricional detalhada",
            "Investigação de possíveis causas metabólicas ou clínicas",
            "Plano alimentar para recuperação ponderal"
        ],
        "Peso Normal": [
            "Manutenção de hábitos alimentares equilibrados",
            "Prática regular de atividade física",
            "Monitoramento periódico do IMC"
        ],
        "Sobrepeso Nível I": [
            "Reeducação alimentar estruturada",
            "Aumento progressivo de atividade física",
            "Monitoramento clínico periódico"
        ],
        "Sobrepeso Nível II": [
            "Intervenção nutricional intensiva",
            "Avaliação metabólica laboratorial",
            "Acompanhamento multiprofissional"
        ],
        "Obesidade Grau I": [
            "Plano terapêutico estruturado",
            "Avaliação cardiometabólica",
            "Acompanhamento nutricional regular"
        ],
        "Obesidade Grau II": [
            "Encaminhamento para equipe multiprofissional",
            "Avaliação endocrinológica",
            "Investigação de comorbidades associadas"
        ],
        "Obesidade Grau III": [
            "Encaminhamento especializado imediato",
            "Avaliação para cirurgia bariátrica conforme critérios clínicos",
            "Acompanhamento psicológico quando indicado"
        ]
    }

    for item in diretrizes.get(resultado_pt, []):
        st.markdown(f"- {item}")

    # Nota bariátrica complementar
    if imc >= 40:
        st.warning("IMC ≥ 40 kg/m²: critério clássico para avaliação de elegibilidade para cirurgia bariátrica.")
