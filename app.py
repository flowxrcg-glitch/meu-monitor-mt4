import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="MT4 Live Monitor", layout="wide", page_icon="📊")

# Estilo CSS para melhorar a aparência
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Monitor de Performance - MetaTrader 4")

# FUNÇÃO PARA CARREGAR DADOS
# Por enquanto, vamos criar dados fictícios para você ver o layout. 
# Depois, trocaremos pelo seu arquivo que a VPS vai enviar.
def load_data():
    # Simulando dados que viriam do MT4
    data = {
        'Horário': pd.date_range(start='2023-10-01', periods=10, freq='H'),
        'Ativo': ['EURUSD', 'GBPUSD', 'XAUUSD', 'BTCUSD', 'EURUSD', 'USDJPY', 'GBPUSD', 'XAUUSD', 'BTCUSD', 'EURUSD'],
        'Tipo': ['Buy', 'Sell', 'Buy', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy'],
        'Lote': [0.01, 0.02, 0.01, 0.05, 0.01, 0.02, 0.01, 0.01, 0.10, 0.01],
        'Lucro': [10.50, -5.20, 25.00, 100.30, -2.10, 15.40, -10.00, 45.00, -80.00, 12.00]
    }
    return pd.DataFrame(data)

df = load_data()

# --- BARRA LATERAL (Filtros) ---
st.sidebar.header("Filtros")
ativo_selecionado = st.sidebar.multiselect("Selecione os Ativos:", df['Ativo'].unique(), default=df['Ativo'].unique())
df_filtrado = df[df['Ativo'].isin(ativo_selecionado)]

# --- MÉTRICAS PRINCIPAIS ---
col1, col2, col3, col4 = st.columns(4)
total_profit = df_filtrado['Lucro'].sum()
win_rate = (len(df_filtrado[df_filtrado['Lucro'] > 0]) / len(df_filtrado)) * 100

col1.metric("Lucro Total", f"$ {total_profit:.2f}", delta=f"{total_profit:.2f}")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Total de Ordens", len(df_filtrado))
col4.metric("Maior Gain", f"$ {df_filtrado['Lucro'].max():.2f}")

# --- GRÁFICOS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Evolução do Saldo (Equity)")
    df_filtrado['Cum_Profit'] = df_filtrado['Lucro'].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtrado['Horário'], y=df_filtrado['Cum_Profit'], 
                             mode='lines+markers', name='Lucro Acumulado',
                             line=dict(color='#00ff00', width=3)))
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Lucro por Ativo")
    profit_by_asset = df_filtrado.groupby('Ativo')['Lucro'].sum().reset_index()
    fig_pie = go.Figure(data=[go.Pie(labels=profit_by_asset['Ativo'], values=profit_by_asset['Lucro'], hole=.3)])
    fig_pie.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TABELA DE DADOS ---
st.subheader("Histórico Detalhado")
st.dataframe(df_filtrado, use_container_width=True)