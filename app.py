import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Configuração inicial do Streamlit
st.title("Análise de Dados Ambientais")
st.write("Este aplicativo permite analisar a média diária de umidade ou temperatura a partir de um arquivo de dados.")

# Upload do arquivo pelo usuário
uploaded_file = st.file_uploader("Faça o upload do arquivo .dat", type=["dat", "csv"])

if uploaded_file:
    try:
        # Carregar o arquivo ignorando as 6 primeiras linhas
        df = pd.read_csv(uploaded_file, sep='\t', skiprows=10, names=["Date", "Time", "Humidity", "Temperature"])

        # Converter a coluna "Date" para o formato datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Verificar se a conversão foi bem-sucedida
        if df['Date'].isnull().all():
            st.error("O arquivo não contém datas válidas. Verifique o formato da coluna 'Date'.")
        else:
            # Remover linhas com valores NaT na coluna 'Date'
            df = df.dropna(subset=['Date'])

            # Seleção de análise: Umidade ou Temperatura
            analysis_type = st.radio("Escolha o tipo de análise:", ("Umidade", "Temperatura"))

            if analysis_type == "Umidade":
                column_to_analyze = "Humidity"
                y_label = "Umidade Média (%)"
                plot_title = "Média Diária de Umidade"
            else:
                column_to_analyze = "Temperature"
                y_label = "Temperatura Média (°C)"
                plot_title = "Média Diária de Temperatura"

            # Remover valores nulos na coluna selecionada
            df = df.dropna(subset=[column_to_analyze])

            # Exibir as datas disponíveis
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()

            st.write(f"Datas disponíveis: **{min_date}** a **{max_date}**")

            # Seleção de intervalo de datas
            start_date = st.date_input("Selecione a data de início", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("Selecione a data de fim", max_date, min_value=min_date, max_value=max_date)

            if start_date > end_date:
                st.error("A data de início deve ser anterior ou igual à data de fim.")
            else:
                # Filtrar o DataFrame com base no intervalo de datas
                mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
                filtered_df = df[mask]

                # Calcular a média diária
                daily_avg = filtered_df.groupby(filtered_df['Date'].dt.date)[column_to_analyze].mean()

                if daily_avg.empty:
                    st.warning("Nenhum dado disponível no intervalo de datas selecionado.")
                else:
                    # Plotar o gráfico
                    fig, ax = plt.subplots(figsize=(10, 6))
                    daily_avg.plot(kind='line', marker='o', linestyle='-', color='b', ax=ax)

                    ax.set_title(plot_title, fontsize=14)
                    ax.set_xlabel('Data', fontsize=12)
                    ax.set_ylabel(y_label, fontsize=12)
                    ax.tick_params(axis='x', rotation=45)
                    ax.grid(True)

                    # Exibir o gráfico no Streamlit
                    st.pyplot(fig)

                    # Botão para baixar o gráfico
                    buffer = BytesIO()
                    fig.savefig(buffer, format='png', dpi=300)
                    buffer.seek(0)

                    st.download_button(
                        label="Baixar Gráfico",
                        data=buffer,
                        file_name=f"media_diaria_{column_to_analyze.lower()}.png",
                        mime="image/png"
                    )
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo para começar a análise.")
