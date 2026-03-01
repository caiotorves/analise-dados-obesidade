import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Health Insights - Apoio à Decisão", layout="centered", page_icon="🏥")

@st.cache_resource
def load_data():
    # Carrega o dicionário que contém o pipeline e a lista de colunas
    artefato = joblib.load("modelo_obesidade.pkl")
    return artefato["pipeline"], artefato["colunas"]

model, colunas_treino = load_data()

label_map = {
    'Insufficient_Weight': 'Baixo Peso', 'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I', 'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I', 'Obesity_Type_II': 'Obesidade Grau II', 'Obesity_Type_III': 'Obesidade Grau III'
}

st.title("🏥 Sistema de Apoio à Decisão Clínica")
st.markdown("Plataforma de Machine Learning para classificação de risco e suporte diagnóstico.")
st.markdown("---")

st.header("Perfil do Paciente")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gênero", ["Male", "Female"], format_func=lambda x: "Masculino" if x == "Male" else "Feminino")
        age = st.number_input("Idade", 1, 100, 25)
        height = st.number_input("Altura (m)", 1.0, 2.5, 1.70, step=0.01)
        weight = st.number_input("Peso (kg)", 10.0, 250.0, 70.0, step=0.1)
        family_history = st.selectbox("Histórico Familiar de Sobrepeso?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")
        favc = st.selectbox("Consome alimentos calóricos com frequência?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")
    with col2:
        fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1.0, 3.0, 2.0)
        ncp = st.slider("Número de refeições principais por dia", 1, 4, 3)
        caec = st.selectbox("Consome alimentos entre as refeições?", ["Sometimes", "Frequently", "Always", "no"], 
                            format_func=lambda x: {"Sometimes":"Às vezes","Frequently":"Frequentemente","Always":"Sempre","no":"Não"}[x])
        smoke = st.selectbox("O paciente fuma?", ["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não")
        faf = st.slider("Atividade Física (0-3)", 0.0, 3.0, 1.0)
        calc = st.selectbox("Consumo de Álcool?", ["no", "Sometimes", "Frequently", "Always"],
                            format_func=lambda x: {"no":"Não","Sometimes":"Às vezes","Frequently":"Frequentemente","Always":"Sempre"}[x])

    submitted = st.form_submit_button("Gerar Diagnóstico")

if submitted:
    # 1. Cálculo do IMC para conferência clínica
    imc = weight / (height ** 2)
    
    # 2. Organização dos dados na ordem exata do treinamento
    input_dict = {
        'Gender': gender, 'Age': age, 'Height': height, 'Weight': weight,
        'family_history': family_history, 'FAVC': favc, 'FCVC': fcvc,
        'NCP': ncp, 'CAEC': caec, 'SMOKE': smoke,
        'CH2O': 2.0, 'SCC': 'no', 'FAF': faf, 'TUE': 1.0,
        'CALC': calc, 'MTRANS': 'Public_Transportation'
    }
    input_data = pd.DataFrame([input_dict])[colunas_treino]
    
    # 3. Predição do Modelo
    prediction = model.predict(input_data)[0]
    resultado_pt = label_map.get(prediction, prediction)

    st.markdown("---")
    st.subheader(f"📌 Resultado do Diagnóstico: {resultado_pt}")
    st.info(f"IMC Calculado: {imc:.2f}")

    # --- 4. INTERPRETAÇÃO CLÍNICA ---
    st.markdown("## 🩺 Interpretação Clínica")
    interpretacoes = {
        "Baixo Peso": "Estado nutricional abaixo da faixa considerada adequada, podendo estar associado a risco de déficit nutricional, redução de massa muscular e possível vulnerabilidade imunológica. Recomenda-se investigação clínica para identificação de causas subjacentes.",
        "Peso Normal": "Estado nutricional dentro da faixa considerada adequada, sem indicativos atuais de risco metabólico relacionado ao peso.",
        "Sobrepeso Nível I": "Excesso de peso leve, com potencial aumento progressivo do risco cardiometabólico, especialmente na presença de outros fatores associados (sedentarismo, histórico familiar, alterações laboratoriais). Requer intervenção preventiva.",
        "Sobrepeso Nível II": "Excesso de peso moderado, com risco aumentado para desenvolvimento de comorbidades como hipertensão arterial, resistência insulínica e dislipidemias. Indica necessidade de acompanhamento clínico estruturado.",
        "Obesidade Grau I": "Obesidade estabelecida, associada a risco significativo para doenças cardiometabólicas, inflamatórias e osteoarticulares. Recomenda-se intervenção multidisciplinar e monitoramento contínuo.",
        "Obesidade Grau II": "Obesidade de grau elevado, com risco substancial para complicações metabólicas, cardiovasculares e redução da qualidade de vida. Necessita abordagem clínica intensiva e acompanhamento regular.",
        "Obesidade Grau III": "Obesidade grave, associada a alto risco de morbidade e mortalidade relacionadas a doenças cardiovasculares, metabólicas e respiratórias. Indica necessidade de manejo especializado e avaliação para terapias avançadas."
    }
    st.write(interpretacoes.get(resultado_pt, ""))
    
    # Observação Técnica exclusiva para Sobrepeso
    if "Sobrepeso" in resultado_pt:
        st.markdown("> **Observação Técnica:** O IMC é um indicador de triagem populacional e não deve ser utilizado isoladamente para diagnóstico. A interpretação deve considerar composição corporal, circunferência abdominal, percentual de gordura, nível de atividade física e perfil metabólico.")

    # --- 5. DIRETRIZES CLÍNICAS ---
    st.markdown("## 📋 Diretrizes Clínicas Sugeridas")
    diretrizes = {
        "Baixo Peso": ["Avaliação nutricional individualizada", "Investigação de causas secundárias", "Solicitação de exames laboratoriais", "Monitoramento periódico", "Encaminhamento para nutricionista", "Avaliação psicológica se necessário"],
        "Peso Normal": ["Orientação para hábitos equilibrados", "Incentivo à atividade física", "Monitoramento periódico do IMC", "Educação em saúde", "Reavaliação anual"],
        "Sobrepeso Nível I": ["Encaminhamento para nutricionista", "Plano alimentar individualizado", "Atividade física (mín. 150 min/semana)", "Avaliação de risco metabólico", "Monitoramento trimestral"],
        "Sobrepeso Nível II": ["Encaminhamento obrigatório para nutricionista", "Avaliação médica para comorbidades", "Exames laboratoriais completos", "Reeducação alimentar estruturada", "Avaliação psicológica", "Reavaliação trimestral"],
        "Obesidade Grau I": ["Avaliação clínica completa", "Acompanhamento multidisciplinar", "Monitoramento de comorbidades", "Mudança intensiva de estilo de vida", "Considerar farmacoterapia", "Reavaliação trimestral"],
        "Obesidade Grau II": ["Avaliação médica detalhada", "Acompanhamento multidisciplinar", "Protocolo estruturado de perda ponderal", "Avaliação para farmacoterapia", "Monitoramento rigoroso", "Reavaliação a cada 2-3 meses"],
        "Obesidade Grau III": ["Avaliação cardiometabólica abrangente", "Acompanhamento especializado", "Avaliação para cirurgia bariátrica", "Monitoramento intensivo", "Acompanhamento psicológico contínuo", "Reavaliação frequente (1-2 meses)"]
    }
    for item in diretrizes.get(resultado_pt, []):
        st.markdown(f"- {item}")

    # Nota Bariátrica (Travada no cálculo matemático do IMC)
    if imc >= 40:
        st.warning("IMC ≥ 40 kg/m²: critério clássico para avaliação de elegibilidade para cirurgia bariátrica.")
