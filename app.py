import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import Row

# Inicializa a sessão Spark
spark = SparkSession.builder.appName("ObesidadeApp").getOrCreate()

# Configuração da página
st.set_page_config(page_title="Diagnóstico Preditivo", layout="centered")
st.title("⚕️ Sistema de Apoio à Decisão Clínica")

# Mapeamento de resultados
label_map = {
    0.0: 'Peso Insuficiente', 1.0: 'Peso Normal', 2.0: 'Sobrepeso Nível I',
    3.0: 'Sobrepeso Nível II', 4.0: 'Obesidade Grau I', 5.0: 'Obesidade Grau II', 
    6.0: 'Obesidade Grau III'
}

# Carrega o modelo (Caminho que criamos no GitHub)
@st.cache_resource
def load_model():
    return PipelineModel.load("modelo_obesidade_spark")

model = load_model()

# Interface Lateral
with st.sidebar:
    st.header("Dados do Paciente")
    age = st.number_input("Idade", 1, 120, 25)
    gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
    height = st.number_input("Altura (m)", 1.0, 2.5, 1.70)
    weight = st.number_input("Peso (kg)", 10.0, 300.0, 70.0)

# Corpo Principal
st.subheader("Hábitos e Histórico")
col1, col2 = st.columns(2)
with col1:
    family = st.selectbox("Histórico Familiar?", ["Sim", "Não"])
    favc = st.selectbox("Alimentos Calóricos?", ["Sim", "Não"])
    fcvc = st.slider("Consumo de vegetais", 1, 3, 2)
    ncp = st.slider("Refeições principais", 1, 4, 3)
with col2:
    caec = st.selectbox("Alimentos entre refeições", ["Sempre", "Frequentemente", "Às vezes", "Não"])
    smoke = st.selectbox("Fumante?", ["Sim", "Não"])
    ch2o = st.slider("Água diária (L)", 1, 3, 2)
    faf = st.slider("Atividade física (Dias)", 0, 3, 1)

if st.button("Gerar Diagnóstico"):
    # Converte entradas para o formato do Spark
    input_data = spark.createDataFrame([Row(
        Gender=gender, Age=float(age), Height=float(height), Weight=float(weight),
        family_history_with_overweight=family, FAVC=favc, FCVC=float(fcvc), NCP=float(ncp),
        CAEC=caec, SMOKE=smoke, CH2O=float(ch2o), FAF=float(faf)
    )])
    
    # Faz a predição
    prediction = model.transform(input_data)
    result_idx = prediction.select("prediction").collect()[0][0]
    
    st.success(f"Diagnóstico: **{label_map[result_idx]}**")
