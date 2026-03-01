import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Health Insights - Apoio à Decisão", layout="centered", page_icon="🏥")

@st.cache_resource
def load_data():
    artefato = joblib.load("modelo_obesidade.pkl")
    return artefato["pipeline"], artefato["colunas"]

model, colunas_treino = load_data()

label_map = {
    'Insufficient_Weight': 'Baixo Peso', 'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I', 'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I', 'Obesity_Type_II': 'Obesidade Grau II', 'Obesity_Type_III': 'Obesidade Grau III'
}

# --- SIDEBAR ORIGINAL REESTABELECIDA ---
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

st.title("🏥 Sistema de Apoio à Decisão Clínica")
st.markdown("Sistema baseado em Machine Learning para classificação do nível de obesidade.")
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
        # ADICIONADOS PARA ELIMINAR O VIÉS DE "PESO NORMAL" EM CASOS GRAVES
        ch2o = st.slider("Consumo de Água Diário (L)", 1.0, 3.0, 2.0)
        calc = st.selectbox("Consumo de Álcool?", ["no", "Sometimes", "Frequently", "Always"],
                            format_func=lambda x: {"no":"Não","Sometimes":"Às vezes","Frequently":"Frequentemente","Always":"Sempre"}[x])

    submitted = st.form_submit_button("Gerar Diagnóstico")

if submitted:
    imc = weight / (height ** 2)
    
    # LÓGICA DE INPUT SEM VALORES FIXOS QUE DISTORCEM O RESULTADO
    input_dict = {
        'Gender': gender, 'Age': age, 'Height': height, 'Weight': weight,
        'family_history': family_history, 'FAVC': favc, 'FCVC': fcvc,
        'NCP': ncp, 'CAEC': caec, 'SMOKE': smoke,
        'CH2O': ch2o, 'SCC': 'no', 'FAF': faf, 'TUE': 1.0,
        'CALC': calc, 'MTRANS': 'Public_Transportation'
    }
    input_data = pd.DataFrame([input_dict])[colunas_treino]
    prediction = model.predict(input_data)[0]
    resultado_pt = label_map.get(prediction, prediction)

    st.markdown("---")
    st.subheader(f"📌 Resultado do Diagnóstico: {resultado_pt}")
    st.info(f"IMC Calculado: {imc:.2f}")

    # --- INTERPRETAÇÃO CLÍNICA (TEXTOS EXATOS) ---
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

    if resultado_pt == "Sobrepeso Nível I":
        st.markdown("**Observação Técnica**")
        st.write("O IMC é um indicador de triagem populacional e não deve ser utilizado isoladamente para diagnóstico. A interpretação deve considerar composição corporal, circunferência abdominal, percentual de gordura, nível de atividade física e perfil metabólico. Indivíduos com elevada massa muscular podem apresentar IMC na faixa de sobrepeso sem aumento real de risco cardiometabólico.")
    
    if resultado_pt == "Sobrepeso Nível II":
        st.markdown("**Observação Técnica**")
        st.write("A classificação pelo IMC deve ser complementada por avaliação clínica individualizada, incluindo análise de composição corporal e marcadores metabólicos, a fim de evitar superestimação de risco em indivíduos fisicamente ativos ou com maior massa muscular.")

    # --- DIRETRIZES CLÍNICAS (TEXTOS EXATOS) ---
    st.markdown("## 📋 Diretrizes Clínicas Sugeridas")
    diretrizes = {
        "Baixo Peso": ["Avaliação nutricional individualizada com plano de readequação calórica e proteica.", "Investigação de possíveis causas secundárias (distúrbios gastrointestinais, endocrinológicos ou psicológicos).", "Solicitação de exames laboratoriais conforme indicação clínica.", "Monitoramento periódico de peso, composição corporal e estado nutricional.", "Encaminhamento para nutricionista.", "Avaliação psicológica, se houver suspeita de transtorno alimentar."],
        "Peso Normal": ["Orientação para manutenção de hábitos alimentares equilibrados.", "Incentivo à prática regular de atividade física.", "Monitoramento periódico do IMC e circunferência abdominal.", "Educação em saúde voltada à prevenção de fatores de risco cardiometabólicos.", "Reavaliação anual ou conforme indicação clínica."],
        "Sobrepeso Nível I": ["Encaminhamento para acompanhamento nutricional estruturado.", "Prescrição de plano alimentar individualizado.", "Incentivo à atividade física regular (mínimo de 150 minutos semanais).", "Avaliação de fatores de risco metabólicos (glicemia, perfil lipídico, PA).", "Monitoramento trimestral de peso e parâmetros metabólicos.", "Educação em mudança de estilo de vida."],
        "Sobrepeso Nível II": ["Encaminhamento obrigatório para nutricionista.", "Avaliação médica para identificação de comorbidades associadas.", "Solicitação de exames laboratoriais completos (perfil lipídico, glicemia, HbA1c, função hepática).", "Implementação de plano estruturado de reeducação alimentar e atividade física supervisionada.", "Avaliação psicológica quando indicado.", "Reavaliação clínica a cada 3 meses."],
        "Obesidade Grau I": ["Avaliação clínica completa e estratificação de risco cardiovascular.", "Encaminhamento para acompanhamento multidisciplinar (nutricionista e educador físico).", "Monitoramento de comorbidades (diabetes, hipertensão, dislipidemia).", "Intervenção intensiva em mudança de estilo de vida.", "Considerar farmacoterapia conforme critérios clínicos.", "Reavaliação trimestral."],
        "Obesidade Grau II": ["Avaliação médica detalhada com investigação de comorbidades associadas.", "Encaminhamento para equipe multidisciplinar (nutricionista, endocrinologista e psicólogo).", "Implementação de protocolo estruturado de perda ponderal.", "Avaliação para farmacoterapia antiobesidade conforme diretrizes vigentes.", "Monitoramento rigoroso de parâmetros metabólicos.", "Reavaliação clínica a cada 2–3 meses."],
        "Obesidade Grau III": ["Avaliação clínica e cardiometabólica abrangente.", "Encaminhamento obrigatório para acompanhamento multidisciplinar especializado.", "Avaliação formal para elegibilidade à cirurgia bariátrica, conforme critérios clínicos.", "Monitoramento intensivo de comorbidades graves.", "Acompanhamento psicológico contínuo.", "Plano estruturado e supervisionado de reeducação alimentar.", "Reavaliação médica frequente (1–2 meses)."]
    }
    for item in diretrizes.get(resultado_pt, []):
        st.markdown(f"- {item}")

    if imc >= 40:
        st.warning("IMC ≥ 40 kg/m²: critério clássico para avaliação de elegibilidade para cirurgia bariátrica.")
