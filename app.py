import streamlit as st

st.set_page_config(page_title="Avaliação Clínica Nutricional", layout="wide")

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("Painel Clínico")
    st.markdown("Sistema de apoio à decisão clínica preventiva.")
    st.markdown("---")
    st.markdown("**Critérios utilizados:**")
    st.markdown("- Classificação OMS por IMC")
    st.markdown("- Escore de risco metabólico comportamental")
    st.markdown("- Diretrizes clínicas preventivas")

# =========================
# FUNÇÕES
# =========================

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Baixo Peso"
    elif 18.5 <= imc < 25:
        return "Eutrofia"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidade Grau I"
    elif 35 <= imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def calcular_risco(hist_familiar, caloricos, vegetais, lanches, fuma, refeicoes):
    score = 0
    
    if hist_familiar == "Sim":
        score += 1
    if caloricos == "Sim":
        score += 1
    if vegetais <= 1:
        score += 1
    if lanches == "Frequentemente":
        score += 1
    if fuma == "Sim":
        score += 1
    if refeicoes >= 4:
        score += 1
        
    return score

def definir_prioridade(imc_class, risco):
    if imc_class == "Eutrofia":
        if risco <= 1:
            return "Baixa"
        else:
            return "Preventiva"
    elif imc_class == "Sobrepeso":
        if risco <= 2:
            return "Moderada"
        else:
            return "Moderada Alta"
    elif "Obesidade" in imc_class:
        if imc_class == "Obesidade Grau III":
            return "Muito Alta"
        else:
            return "Alta"
    else:
        return "Moderada"

# =========================
# INTERFACE PRINCIPAL
# =========================

st.title("Perfil do Paciente")

col1, col2 = st.columns(2)

with col1:
    genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    idade = st.number_input("Idade", min_value=10, max_value=100, value=25)
    altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.75)
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0)
    hist_familiar = st.selectbox("Histórico Familiar de Sobrepeso?", ["Sim", "Não"])

with col2:
    caloricos = st.selectbox("Consome alimentos calóricos com frequência?", ["Sim", "Não"])
    vegetais = st.slider("Frequência de consumo de vegetais (1-3)", 1, 3, 2)
    refeicoes = st.slider("Número de refeições principais por dia", 1, 6, 3)
    lanches = st.selectbox("Consome alimentos entre as refeições?", ["Raramente", "Às vezes", "Frequentemente"])
    fuma = st.selectbox("O paciente fuma?", ["Sim", "Não"])

if st.button("Gerar Diagnóstico"):

    imc = calcular_imc(peso, altura)
    imc_class = classificar_imc(imc)
    risco = calcular_risco(hist_familiar, caloricos, vegetais, lanches, fuma, refeicoes)
    prioridade = definir_prioridade(imc_class, risco)

    st.markdown("---")
    st.header(f"Resultado do Diagnóstico: {imc_class}")
    st.info(f"IMC Calculado: {imc:.2f}")

    # =========================
    # PRIORIDADE CLÍNICA
    # =========================
    st.subheader("Prioridade Clínica")
    st.warning(f"Nível de Prioridade: {prioridade}")

    # =========================
    # INTERPRETAÇÃO CLÍNICA
    # =========================
    st.subheader("Interpretação Clínica")

    if imc_class == "Eutrofia":
        st.write("Paciente com peso adequado para altura.")
    elif imc_class == "Sobrepeso":
        st.write("Excesso de peso com risco aumentado para doenças metabólicas.")
    else:
        st.write("Obesidade associada a risco significativo cardiovascular e metabólico.")

    # =========================
    # DIRETRIZES
    # =========================
    st.subheader("Diretrizes Clínicas Sugeridas")

    if prioridade in ["Baixa"]:
        st.markdown("- Manutenção de hábitos saudáveis")
        st.markdown("- Reavaliação anual")
    elif prioridade in ["Preventiva"]:
        st.markdown("- Orientação nutricional preventiva")
        st.markdown("- Incentivo à atividade física regular")
        st.markdown("- Monitoramento semestral")
    elif prioridade in ["Moderada", "Moderada Alta"]:
        st.markdown("- Encaminhamento para nutricionista")
        st.markdown("- Plano alimentar estruturado")
        st.markdown("- Monitoramento trimestral")
    else:
        st.markdown("- Avaliação médica especializada")
        st.markdown("- Investigação de comorbidades")
        st.markdown("- Considerar avaliação para tratamento intensivo")

    # =========================
    # ADENDOS
    # =========================
    st.subheader("Adendos Clínicos")

    st.markdown(f"• Escore de risco metabólico: {risco}/6")
    st.markdown("• A prioridade considera IMC + fatores comportamentais.")
    st.markdown("• Este sistema não substitui avaliação médica presencial.")
