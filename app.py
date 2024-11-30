import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial do Streamlit
st.title("Análise de Umidade Diária")
st.write("Este aplicativo permite analisar a média diária de umidade a partir de um arquivo de dados.")

# Upload do arquivo pelo usuário
uploaded_file = st.file_uploader("Faça o upload do arquivo .dat", type=["dat", "csv"])

if uploaded_file:
    try:
        # Carregar o arquivo ignorando as 6 primeiras linhas
        df = pd.read_csv(uploaded_file, sep='\t', skiprows=10, names=["Date", "Time", "Humidity"])

        # Converter a coluna "Date" para o formato datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Remover valores nulos
        df = df.dropna(subset=['Date', 'Humidity'])

        # Calcular a média diária de umidade
        daily_avg = df.groupby(df['Date'].dt.date)['Humidity'].mean()

        if daily_avg.empty:
            st.warning("Nenhum dado disponível para plotar o gráfico.")
        else:
            # Plotar o gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            daily_avg.plot(kind='line', marker='o', linestyle='-', color='b', ax=ax)

            ax.set_title('Média Diária de Umidade', fontsize=14)
            ax.set_xlabel('Data', fontsize=12)
            ax.set_ylabel('Umidade Média (%)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)

            # Exibir o gráfico no Streamlit
            st.pyplot(fig)

            # Botão para baixar o gráfico
            from io import BytesIO

            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=300)
            buffer.seek(0)

            st.download_button(
                label="Baixar Gráfico",
                data=buffer,
                file_name="media_diaria_umidade.png",
                mime="image/png"
            )
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo para começar a análise.")
