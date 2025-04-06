import streamlit as st
import pandas as pd
import psycopg2
from urllib.parse import urlparse
import plotly.express as px

# ============== CONEXIÓN A LA BASE DE DATOS ==================
DATABASE_URL = "postgresql://postgres:caZQnWYDDpWxUBoZroiFnQMzfQifVghQ@hopper.proxy.rlwy.net:36834/railway"
url = urlparse(DATABASE_URL)
conn_params = {
    "host": url.hostname,
    "user": url.username,
    "password": url.password,
    "dbname": url.path[1:],
    "port": url.port
}

@st.cache_data
def cargar_datos():
    try:
        conn = psycopg2.connect(**conn_params)
        df_cultivos = pd.read_sql("SELECT * FROM cultivos", conn)
        conn.close()
        return df_cultivos
    except Exception as e:
        st.error(f"❌ Error al conectar a la base de datos: {e}")
        return pd.DataFrame()

# ============== DASHBOARD ==================
st.set_page_config(page_title="🌾 Producción de Cultivos", layout="wide")
st.title("📦 Producción y Rendimiento de Cultivos por Municipio")

df = cargar_datos()

if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y", errors="coerce")

    # Filtros
    col1, col2, col3 = st.columns(3)
    cultivo_filtro = col1.multiselect("🧪 Cultivo", df["nombre_cultivo"].dropna().unique())
    mpio_filtro = col2.multiselect("🏡 Municipio", df["municipio"].dropna().unique())
    periodo_filtro = col3.multiselect("📅 Periodo", df["periodo"].dropna().unique())

    # Aplicar filtros
    df_filtrado = df.copy()
    if cultivo_filtro:
        df_filtrado = df_filtrado[df_filtrado["nombre_cultivo"].isin(cultivo_filtro)]
    if mpio_filtro:
        df_filtrado = df_filtrado[df_filtrado["municipio"].isin(mpio_filtro)]
    if periodo_filtro:
        df_filtrado = df_filtrado[df_filtrado["periodo"].isin(periodo_filtro)]

    # Mostrar tabla filtrada
    st.dataframe(df_filtrado)

    if not df_filtrado.empty:
        # ====== 1. Producción total por municipio y cultivo ======
        st.subheader("📦 Producción total por Municipio y Cultivo")
        df_grouped = df_filtrado.groupby(["municipio", "nombre_cultivo"])["produccion_ton"].sum().reset_index()

        fig1 = px.bar(df_grouped,
                      x="municipio",
                      y="produccion_ton",
                      color="nombre_cultivo",
                      title="Producción total por municipio y cultivo (toneladas)",
                      labels={
                          "produccion_ton": "Producción (ton)",
                          "municipio": "Municipio",
                          "nombre_cultivo": "Cultivo"
                      },
                      color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig1, use_container_width=True)

        # ====== 2. Área cosechada por municipio ======
        st.subheader("🌾 Área cosechada total por Municipio")
        df_area = df_filtrado.groupby("municipio")["area_cosechada"].sum().reset_index().sort_values(by="area_cosechada", ascending=False)

        fig2 = px.bar(df_area,
                      x="municipio",
                      y="area_cosechada",
                      title="Área cosechada total por municipio (ha)",
                      labels={
                          "area_cosechada": "Área cosechada (ha)",
                          "municipio": "Municipio"
                      },
                      color_discrete_sequence=["#A3C4DC"])
        st.plotly_chart(fig2, use_container_width=True)

        # ====== 3. Top 10 municipios por rendimiento promedio general ======
        st.subheader("🏆 Top 10 Municipios por Rendimiento Promedio (t/ha)")

        df_rend_top10 = (
            df_filtrado.groupby("municipio")["rendimiento_t_ha"]
            .mean()
            .reset_index()
            .sort_values(by="rendimiento_t_ha", ascending=False)
            .head(10)
        )

        fig3 = px.bar(df_rend_top10,
                      x="municipio",
                      y="rendimiento_t_ha",
                      title="Top 10 Municipios con Mayor Rendimiento Promedio (t/ha)",
                      labels={
                          "rendimiento_t_ha": "Rendimiento Promedio (t/ha)",
                          "municipio": "Municipio"
                      },
                      text_auto=".2f",
                      color="municipio",
                      color_discrete_sequence=px.colors.qualitative.Set2)

        fig3.update_layout(
            xaxis_title="Municipio",
            yaxis_title="Rendimiento (t/ha)",
            showlegend=False,
            height=500,
            margin=dict(t=50, b=50)
        )

        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
else:
    st.warning("⚠️ No se pudieron cargar los datos de cultivos.")
