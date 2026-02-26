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

    prediction = model.predict(input_data)[0]
    resultado_pt = label_map.get(prediction, prediction)

    imc = weight / (height ** 2)

    st.subheader(f"Resultado do Diagnóstico: {resultado_pt}")
    st.info(f"IMC Calculado: {imc:.2f}")

    # ----------------------------
    # INTERPRETAÇÃO CLÍNICA
    # ----------------------------

    st.markdown("## Interpretação Clínica")

    interpretacoes = {
        "Peso Normal": "Estado nutricional dentro da faixa considerada adequada. Não há indicativos atuais de risco metabólico relacionado ao peso.",
        "Sobrepeso Nível I": "Excesso de peso com potencial risco metabólico futuro. Condição associada a maior probabilidade de desenvolvimento de comorbidades se não houver intervenção precoce.",
        "Sobrepeso Nível II": "Excesso de peso significativo com risco metabólico aumentado. Requer intervenção preventiva estruturada.",
        "Obesidade Grau I": "Obesidade estabelecida com risco aumentado para doenças cardiovasculares e metabólicas. Requer intervenção estruturada.",
        "Obesidade Grau II": "Obesidade moderada a grave com risco elevado de complicações metabólicas, cardiovasculares e osteoarticulares. Necessita abordagem multiprofissional.",
        "Obesidade Grau III": "Obesidade grave com risco significativo à saúde e alta probabilidade de complicações sistêmicas. Condição que exige abordagem especializada e intensiva."
    }

    st.write(interpretacoes.get(resultado_pt, ""))

    # ----------------------------
    # DIRETRIZES CLÍNICAS
    # ----------------------------

    st.markdown("## Diretrizes Clínicas Sugeridas")

    diretrizes = {
        "Peso Normal": [
            "Manutenção de hábitos alimentares equilibrados",
            "Incentivo à prática regular de atividade física",
            "Monitoramento anual do IMC",
            "Educação preventiva em saúde"
        ],
        "Sobrepeso Nível I": [
            "Encaminhamento para avaliação nutricional",
            "Elaboração de plano alimentar estruturado",
            "Incentivo à atividade física supervisionada",
            "Monitoramento trimestral de peso e IMC"
        ],
        "Sobrepeso Nível II": [
            "Encaminhamento para avaliação nutricional",
            "Plano alimentar estruturado",
            "Atividade física supervisionada",
            "Reavaliação periódica"
        ],
        "Obesidade Grau I": [
            "Encaminhamento obrigatório para nutricionista",
            "Avaliação de comorbidades (glicemia, perfil lipídico, pressão arterial)",
            "Prescrição de atividade física supervisionada",
            "Reavaliação clínica em até 3 meses"
        ],
        "Obesidade Grau II": [
            "Encaminhamento para nutricionista",
            "Encaminhamento para endocrinologista",
            "Investigação ativa de diabetes mellitus, hipertensão arterial e dislipidemias",
            "Avaliação multiprofissional estruturada",
            "Monitoramento clínico periódico"
        ],
        "Obesidade Grau III": [
            "Encaminhamento para equipe multiprofissional especializada",
            "Avaliação endocrinológica completa",
            "Investigação de comorbidades graves",
            "Avaliação para elegibilidade de cirurgia bariátrica conforme critérios clínicos",
            "Acompanhamento psicológico quando indicado"
        ]
    }

    for item in diretrizes.get(resultado_pt, []):
        st.markdown(f"- {item}")

    if imc >= 40:
        st.warning("IMC ≥ 40 kg/m²: Critério clássico para avaliação de elegibilidade para cirurgia bariátrica conforme diretrizes clínicas.")

    # ----------------------------
    # FATORES ADICIONAIS DE ATENÇÃO
    # ----------------------------

    st.markdown("## Fatores Adicionais de Atenção")

    fatores = []

    if age >= 60:
        fatores.append("Idade ≥ 60 anos associada a maior risco cardiovascular e metabólico.")

    if family_history == "yes":
        fatores.append("Presença de histórico familiar de sobrepeso/obesidade.")

    if favc == "yes":
        fatores.append("Consumo frequente de alimentos calóricos.")

    if fcvc <= 1.5:
        fatores.append("Baixa frequência de consumo de vegetais.")

    if smoke == "yes":
        fatores.append("Tabagismo como fator agravante cardiovascular.")

    if fatores:
        for f in fatores:
            st.markdown(f"- {f}")
    else:
        st.write("Nenhum fator adicional de risco identificado além da classificação principal.")
