import streamlit as st
import pandas as pd
import psycopg2
from urllib.parse import urlparse

# ================== CONFIGURACIÓN BASE DE DATOS ==================

# URL completa de PostgreSQL (copiada de Railway)
DATABASE_URL = "postgresql://postgres:caZQnWYDDpWxUBoZroiFnQMzfQifVghQ@hopper.proxy.rlwy.net:36834/railway"
url = urlparse(DATABASE_URL)

# Parámetros de conexión
conn_params = {
    "host": url.hostname,
    "user": url.username,
    "password": url.password,
    "dbname": url.path[1:],  # quita el '/' inicial
    "port": url.port
}

# ================== CONEXIÓN Y CONSULTA ==================

@st.cache_data
def cargar_datos():
    try:
        conn = psycopg2.connect(**conn_params)
        df_cultivos = pd.read_sql("SELECT * FROM cultivos LIMIT 100", conn)
        df_clima = pd.read_sql("SELECT * FROM clima LIMIT 100", conn)
        conn.close()
        return df_cultivos, df_clima
    except Exception as e:
        st.error(f"❌ Error al conectar a la base de datos: {e}")
        return pd.DataFrame(), pd.DataFrame()

# ================== INTERFAZ STREAMLIT ==================

st.set_page_config(page_title="Dashboard Agricultura y Clima", layout="wide")
st.title("🌱 Dashboard Agricultura y Clima")

df_cultivos, df_clima = cargar_datos()

# Tabs para separar vistas
tab1, tab2 = st.tabs(["📊 Cultivos", "🌦️ Clima"])

with tab1:
    st.subheader("📋 Datos de Cultivos")
    if not df_cultivos.empty:
        st.dataframe(df_cultivos)
    else:
        st.warning("No se pudieron cargar los datos de cultivos.")

with tab2:
    st.subheader("🌧️ Datos de Clima")
    if not df_clima.empty:
        st.dataframe(df_clima)
    else:
        st.warning("No se pudieron cargar los datos de clima.")
