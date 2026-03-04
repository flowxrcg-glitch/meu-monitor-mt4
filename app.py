import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 1. Suas chaves (Pegue no Supabase > Settings > API)
URL = "https://jxhxbwgebugoumvdcauq.supabase.com"
KEY = "sb_publishable_CFuI4WNUUlLypU4n08VqGw_RDLt_pG-"
supabase = create_client(URL, KEY)

# 2. Atualiza o site sozinho a cada 5 segundos
st_autorefresh(interval=5000, key="flowx_refresh")

st.markdown("<h1 style='color: #a020f0;'>💜 FLOWX | GTA Monitor</h1>", unsafe_allow_html=True)

# 3. Puxa os dados do banco
try:
    data = supabase.table("trading_signals").select("*").execute()
    df = pd.DataFrame(data.data)
    if not df.empty:
        st.table(df.sort_values("moeda")) # Mostra a tabela organizada
    else:
        st.write("Aguardando dados da VPS...")
except Exception as e:
    st.error(f"Erro de conexão: {e}")

