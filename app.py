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
para classificação do nível de obesidade com integração
de estratificação de risco clínico.
""")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 🔎 Estrutura Analítica

- Classificação preditiva  
- Cálculo de IMC  
- Interpretação clínica  
- Diretrizes sugeridas  
- Fatores agravantes  
- Prioridade clínica baseada em estratificação  
""")

st.sidebar.markdown("---")
st.sidebar.caption("Projeto Acadêmico – Data Science aplicada à Saúde")

# ----------------------------
# INTERFACE
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
    # INTERPRETAÇÃO
    # ----------------------------

    st.markdown("## 🩺 Interpretação Clínica")

    interpretacoes = {
        "Peso Normal": "Estado nutricional dentro da faixa considerada adequada.",
        "Sobrepeso Nível I": "Excesso de peso com potencial risco metabólico futuro.",
        "Sobrepeso Nível II": "Excesso de peso significativo com risco metabólico aumentado.",
        "Obesidade Grau I": "Obesidade estabelecida com risco aumentado para doenças cardiovasculares e metabólicas.",
        "Obesidade Grau II": "Obesidade moderada a grave com risco elevado de complicações metabólicas.",
        "Obesidade Grau III": "Obesidade grave com risco significativo à saúde."
    }

    st.write(interpretacoes.get(resultado_pt, ""))

    # ----------------------------
    # DIRETRIZES COMPLETAS
    # ----------------------------

    st.markdown("## 📋 Diretrizes Clínicas Sugeridas")

    diretrizes = {
        "Baixo Peso": [
            "Avaliação nutricional detalhada",
            "Investigação de causas metabólicas ou alimentares",
            "Plano alimentar para recuperação ponderal"
        ],
        "Peso Normal": [
            "Manutenção de hábitos alimentares equilibrados",
            "Atividade física regular",
            "Monitoramento periódico do IMC"
        ],
        "Sobrepeso Nível I": [
            "Reeducação alimentar estruturada",
            "Início de programa de atividade física supervisionada",
            "Monitoramento trimestral"
        ],
        "Sobrepeso Nível II": [
            "Intervenção nutricional intensiva",
            "Avaliação metabólica laboratorial",
            "Acompanhamento multiprofissional"
        ],
        "Obesidade Grau I": [
            "Plano terapêutico estruturado",
            "Avaliação cardiometabólica",
            "Acompanhamento multiprofissional"
        ],
        "Obesidade Grau II": [
            "Encaminhamento para equipe multiprofissional",
            "Avaliação endocrinológica",
            "Investigação de comorbidades associadas"
        ],
        "Obesidade Grau III": [
            "Encaminhamento especializado",
            "Avaliação para cirurgia bariátrica conforme critérios clínicos",
            "Acompanhamento psicológico"
        ]
    }

    for item in diretrizes.get(resultado_pt, []):
        st.markdown(f"- {item}")

    # ----------------------------
    # PRIORIDADE CLÍNICA AJUSTADA
    # ----------------------------

    st.markdown("## 🔎 Prioridade Clínica")

    score = 0

    base_score = {
        "Peso Normal": 0,
        "Sobrepeso Nível I": 1,
        "Sobrepeso Nível II": 2,
        "Obesidade Grau I": 3,
        "Obesidade Grau II": 4,
        "Obesidade Grau III": 5
    }

    score += base_score.get(resultado_pt, 0)

    if age >= 60:
        score += 1
    if family_history == "yes":
        score += 1
    if favc == "yes":
        score += 1
    if fcvc <= 1.5:
        score += 1
    if smoke == "yes":
        score += 1

    if score <= 1:
        prioridade = "Baixa"
        cor = "green"
    elif score <= 3:
        prioridade = "Moderada"
        cor = "blue"
    elif score <= 5:
        prioridade = "Alta"
        cor = "orange"
    else:
        prioridade = "Muito Alta"
        cor = "red"

    st.markdown(f"<h3 style='color:{cor};'>Nível: {prioridade}</h3>", unsafe_allow_html=True)

    st.caption("Nota Técnica: A estratificação da Prioridade Clínica considera a gravidade do estado nutricional e a presença de fatores agravantes clínicos e comportamentais, com base em critérios de risco metabólico.")
