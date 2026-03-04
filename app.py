import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="FLOWX GTA Monitor", layout="wide")

# Função para estilizar as células como o MT4
def color_signal(val):
    if "FORÇA" in str(val) or "ALTA" in str(val): color = '#00ff96' # Verde FlowX
    elif "QUEDA" in str(val) or "BAIXA" in str(val): color = '#ff2d50' # Vermelho FlowX
    else: color = '#78787d' # Muted
    return f'background-color: {color}; color: black; font-weight: bold'

st.title("💜 FLOWX | GTA Ultra Fractal - Live Mirror")

# Simulando a leitura do banco de dados que a VPS vai alimentar
# (Depois conectaremos o SQLite aqui)
try:
    # Exemplo de como os dados chegarão via Pandas
    data = {
        'Moeda': ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD'],
        'MN1': [0.15, -0.22, 0.05, -0.40, 0.10, 0.02, -0.01, 0.12],
        'W1': [0.25, -0.10, 0.12, -0.35, 0.08, 0.05, -0.05, 0.15],
        'D1': [0.30, 0.05, 0.20, -0.30, 0.15, 0.08, -0.10, 0.20],
        'H4': [0.22, 0.12, 0.25, -0.20, 0.18, 0.10, -0.15, 0.25],
        'H1': [0.18, 0.15, 0.30, -0.15, 0.20, 0.12, -0.20, 0.30],
        'SINAL': ['FORÇA TOTAL', 'AGUARDE', 'PERMISSÃO ALTA', 'QUEDA TOTAL', 'AGUARDE', 'AGUARDE', 'RETORNO OK', 'FORÇA']
    }
    df = pd.DataFrame(data)

    # Exibição do Dashboard
    st.subheader("Painel de Força de Moedas (CSS)")
    
    # Aplicando estilo de cores nas colunas
    styled_df = df.style.applymap(color_signal, subset=['SINAL'])
    
    st.table(styled_df)

except Exception as e:
    st.error("Aguardando conexão com a VPS...")

st.info("Atualizado em tempo real via MT4 WebRequest")
