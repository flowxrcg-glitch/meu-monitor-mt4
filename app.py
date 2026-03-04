import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 1. Suas chaves (Mantenha as que você já tem)
URL = "https://jxhxbwgebugoumvdcauq.supabase.co"
KEY = "sb_publishable_CFuI4WNUUlLypU4n08VqGw_RDLt_pG-"
supabase = create_client(URL, KEY)

# 2. Configuração da Página e Tema Preto
st.set_page_config(page_title="Painel FlowX", layout="wide")

# CSS para forçar o fundo preto e textos claros
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header { visibility: hidden; }
    .stTable { background-color: #000000; color: #ffffff; }
    h1 { color: #ffffff; font-family: 'Segoe UI'; }
    </style>
    """, unsafe_allow_html=True)

# 3. Atualiza o site sozinho a cada 10 segundos
st_autorefresh(interval=10000, key="flowx_refresh")

st.markdown("<h1>Painel FlowX</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)

# 4. Puxa os últimos dados gravados no banco
try:
    # Buscamos todos os dados da tabela
    response = supabase.table("trading_signals").select("*").execute()
    df = pd.DataFrame(response.data)

    if not df.empty:
        # Organiza por moeda (A-Z)
        df = df.sort_values("moeda")
        
        # Renomeia as colunas para ficar mais amigável no painel
        df.columns = ["Moeda", "MN1", "W1", "D1", "H4", "H1", "Sinal"]
        
        # Exibe a tabela
        st.table(df)
        
        st.success("Conectado: Exibindo últimos dados recebidos da VPS.")
    else:
        st.warning("O banco de dados está vazio. Aguardando a abertura do mercado para receber novos dados.")

except Exception as e:
    st.error(f"Erro ao acessar o banco de dados: {e}")
