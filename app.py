import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 1. Suas chaves (Não mude nada aqui)
URL = "https://jxhxbwgebugoumvdcauq.supabase.co"
KEY = "sb_publishable_CFuI4WNUUlLypU4n08VqGw_RDLt_pG-"
supabase = create_client(URL, KEY)

# 2. Configuração da Página e Tema Preto
st.set_page_config(page_title="Painel FlowX", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    .stTable { background-color: #000000 !important; color: #ffffff !important; }
    h1 { color: #ffffff !important; font-family: 'Segoe UI'; }
    p { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

# Atualiza o site sozinho a cada 5 segundos
st_autorefresh(interval=5000, key="flowx_refresh")

st.markdown("<h1>Painel FlowX</h1>", unsafe_allow_html=True)
st.markdown("<p>Monitoramento em tempo real via VPS</p>", unsafe_allow_html=True)

# 3. Puxa os dados
try:
    response = supabase.table("trading_signals").select("*").execute()
    
    if response.data:
        df = pd.DataFrame(response.data)
        
        # --- O PULO DO GATO PARA CORRIGIR O ERRO ---
        # Aqui a gente seleciona APENAS as colunas que o seu MT4 envia
        colunas_que_queremos = ["moeda", "mn1", "w1", "d1", "h4", "h1", "sinal"]
        
        # Filtra o DataFrame para pegar só essas 7 (ignora id ou created_at)
        df = df[colunas_que_queremos]
        
        # Agora sim renomeamos sem erro, pois garantimos que só existem 7 colunas
        df.columns = ["Moeda", "MN1", "W1", "D1", "H4", "H1", "Sinal"]
        
        # Organiza de A-Z e exibe
        st.table(df.sort_values("Moeda"))
        
    else:
        st.info("Banco de dados conectado. Aguardando a primeira entrega de dados do MetaTrader...")

except Exception as e:
    st.error(f"Erro técnico: {e}")
