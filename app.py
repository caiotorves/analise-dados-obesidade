import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import Row

# Inicialização da Sessão Spark com configurações de compatibilidade para arquivos renomeados
spark = SparkSession.builder.appName("ObesidadeApp").getOrCreate()
spark.conf.set("spark.sql.parquet.enableVectorizedReader", "false")
spark.conf.set("spark.sql.sources.commitProtocolClass", "org.apache.spark.sql.execution.datasources.SQLHadoopMapReduceCommitProtocol")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")

# Configuração da interface visual
st.set_page_config(page_title="Diagnóstico Preditivo de Obesidade", layout="centered")
st.title("⚕️ Sistema de Apoio à Decisão Clínica")
st.markdown("Insira os dados do paciente para obter o diagnóstico preditivo.")

# Mapeamento técnico das classes do modelo
label_map = {
    0.0: 'Peso Insuficiente',
    1.0: 'Peso Normal',
    2.0: 'Sobrepeso Nível I',
    3.0: 'Sobrepeso Nível II',
    4.0: 'Obesidade Grau I',
    5.0: 'Obesidade Grau II',
    6.0: 'Obesidade Grau III'
}

# Carregamento do modelo treinado
@st.cache_resource
def load_model():
    return PipelineModel.load("modelo_obesidade_spark")

model = load_model()

# Interface lateral para coleta de dados demográficos
with st.sidebar:
    st.header("Dados do Paciente")
    age = st.number_input("Idade", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
    height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
    weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0)

# Corpo principal para coleta de hábitos e histórico
st.subheader("Hábitos e Histórico")
col1, col2 = st.columns(2)

with col1:
    family_history = st.selectbox("Histórico Familiar de Sobrepeso?", ["Sim", "Não"])
    favc = st.selectbox("Consumo frequente de alimentos calóricos?", ["Sim", "Não"])
    fcvc = st.slider("Frequência de consumo de vegetais (1-3)", 1.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais", 1.0, 4.0, 3.0)

with col2:
    caec = st.selectbox("Consumo de alimentos entre refeições", ["Sempre", "Frequentemente", "Às vezes", "Não"])
    smoke = st.selectbox("Fumante?", ["Sim", "Não"])
    ch2o = st.slider("Consumo de água diário (Litros)", 1.0, 3.0, 2.0)
    faf = st.slider("Frequência de atividade física (Dias/Semana)", 0.0, 3.0, 1.0)

# Processamento da predição
if st.button("Gerar Diagnóstico"):
    input_data = spark.createDataFrame([Row(
        Gender=gender,
        Age=float(age),
        Height=float(height),
        Weight=float(weight),
        family_history_with_overweight=family_history,
        FAVC=favc,
        FCVC=float(fcvc),
        NCP=float(ncp),
        CAEC=caec,
        SMOKE=smoke,
        CH2O=float(ch2o),
        FAF=float(faf)
    )])
    
    prediction = model.transform(input_data)
    result_idx = prediction.select("prediction").collect()[0][0]
    
    st.success(f"Diagnóstico calculado: **{label_map[result_idx]}**")
