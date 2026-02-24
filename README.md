# 🏥 Sistema Preditivo de Apoio à Decisão Médica - Obesidade

Este repositório contém uma solução completa de Machine Learning para auxiliar equipes médicas no diagnóstico preditivo de níveis de obesidade. O projeto abrange desde o processamento de dados (ETL) até o deploy de uma aplicação interativa.

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Processamento de Dados:** Pandas
* **Machine Learning:** Scikit-learn (Random Forest Classifier)
* **Interface e Deploy:** Streamlit
* **Visualização de Dados:** Power BI

## 📊 Performance do Modelo
O modelo alcançou uma assertividade de **94.09%** na classificação de níveis de obesidade, utilizando um pipeline otimizado que integra pré-processamento de variáveis categóricas e numéricas.

## 📂 Estrutura do Repositório
* `app.py`: Código fonte da aplicação Streamlit.
* `modelo_obesidade.pkl`: Pipeline do modelo treinado e exportado.
* `requirements.txt`: Dependências necessárias para execução do projeto.
* `base_obesidade_traduzida.csv`: Dataset tratado e traduzido para uso no Power BI.
* `importancia_atributos.csv`: Extração da relevância de cada atributo para o diagnóstico.

## 🛠️ Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute a aplicação: `streamlit run app.py`
