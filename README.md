# Sistema de Diagnóstico Preditivo de Obesidade

Plataforma de análise preditiva voltada para a área da saúde, especificamente para o diagnóstico de níveis de obesidade. Desenvolvi uma solução que utiliza algoritmos de aprendizado de máquina treinados em ambiente Big Data para fornecer resultados rápidos e precisos com base em parâmetros clínicos e hábitos de vida dos pacientes.

## Desenvolvimento Técnico
* **Processamento**: Realizei o ETL e a curadoria de dados utilizando PySpark.
* **Modelagem**: Implementei um algoritmo de Random Forest, alcançando uma acurácia de 87,90%.
* **Interface**: Desenvolvi uma aplicação interativa utilizando Streamlit para facilitar o consumo do modelo em ambiente clínico.

## Estrutura de Arquivos
* `app.py`: Script da interface web.
* `modelo_obesidade_spark`: Diretório contendo os artefatos do modelo treinado.
* `requirements.txt`: Dependências do ambiente.

## Como Executar
Configurei o deploy automático via Streamlit Cloud. O sistema recebe variáveis como idade, peso, altura e hábitos alimentares para retornar o diagnóstico em tempo real.
