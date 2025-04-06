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

<<<<<<< HEAD
    else:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
else:
    st.warning("⚠️ No se pudieron cargar los datos de cultivos.")
=======
    # Formulario para agregar tarea
    with st.form("Agregar Tarea"):
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        fecha_limite = st.date_input("Fecha Límite")
        responsable_nombre = st.selectbox("Responsable", [usuario.nombre for usuario in st.session_state.usuarios])
        estado_seleccionado = st.selectbox("Estado", Estado.ESTADOS_VALIDOS)
        submit_button = st.form_submit_button("Agregar Tarea")

        if submit_button:
            responsable = next((u for u in st.session_state.usuarios if u.nombre == responsable_nombre), None)
            fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tarea = Tarea(
                st.session_state.contador_tarea_id,
                titulo,
                descripcion,
                fecha_creacion,
                fecha_limite.strftime('%Y-%m-%d'),
                responsable,
                estado_seleccionado
            )
            st.session_state.tareas.append(tarea)
            st.success(f"✅ Tarea '{titulo}' creada con ID: {st.session_state.contador_tarea_id}")
            st.session_state.contador_tarea_id += 1

            # Mostrar solo la última tarea agregada
            st.subheader("🆕 Última Tarea Creada")
            st.markdown(f"""
            ---
            **🆔 ID:** {tarea.tarea_id}  
            **📌 Título:** {tarea.titulo}  
            **📝 Descripción:** {tarea.descripcion}  
            **👤 Responsable:** {tarea.responsable.nombre}  
            **📅 Fecha límite:** {tarea.fecha_limite}  
            **📈 Estado:** {tarea.estado}
            """)

    # Opciones para Modificar y Eliminar tareas solo si hay tareas creadas
    if st.session_state.tareas:
        st.subheader("✏️ Modificar Tarea")
        tarea_modificar = st.selectbox("Selecciona tarea para modificar", [f"{t.tarea_id} - {t.titulo}" for t in st.session_state.tareas])
        tarea_seleccionada = next((t for t in st.session_state.tareas if t.tarea_id == int(tarea_modificar.split(" - ")[0])), None)

        if tarea_seleccionada:
            nuevo_titulo = st.text_input("Nuevo título", tarea_seleccionada.titulo)
            nueva_descripcion = st.text_area("Nueva descripción", tarea_seleccionada.descripcion)
            nueva_fecha_limite = st.date_input("Nueva fecha límite", datetime.strptime(tarea_seleccionada.fecha_limite, '%Y-%m-%d'))
            nuevo_estado = st.selectbox("Nuevo estado", Estado.ESTADOS_VALIDOS, index=Estado.ESTADOS_VALIDOS.index(tarea_seleccionada.estado))
            nuevo_responsable = st.selectbox("Nuevo responsable", [usuario.nombre for usuario in st.session_state.usuarios], index=[u.nombre for u in st.session_state.usuarios].index(tarea_seleccionada.responsable.nombre))

            if st.button("Guardar Cambios"):
                tarea_seleccionada.titulo = nuevo_titulo
                tarea_seleccionada.descripcion = nueva_descripcion
                tarea_seleccionada.fecha_limite = nueva_fecha_limite.strftime('%Y-%m-%d')
                tarea_seleccionada.estado = nuevo_estado
                tarea_seleccionada.responsable = next((u for u in st.session_state.usuarios if u.nombre == nuevo_responsable), tarea_seleccionada.responsable)
                st.success("🔄 Tarea modificada exitosamente.")

        st.subheader("🗑️ Eliminar Tarea")
        tarea_eliminar = st.selectbox("Selecciona tarea para eliminar", [f"{t.tarea_id} - {t.titulo}" for t in st.session_state.tareas])
        if st.button("Eliminar Tarea"):
            tarea_id_a_eliminar = int(tarea_eliminar.split(" - ")[0])
            st.session_state.tareas = [t for t in st.session_state.tareas if t.tarea_id != tarea_id_a_eliminar]
            st.success("🗑️ Tarea eliminada exitosamente.")


def main():
    st.title("📝 Sistema de Gestión de Tareas")

    # Menú con botones visibles en el sidebar
    st.sidebar.title("📌 Menú Principal")

    if st.sidebar.button("🏠 Inicio"):
        st.session_state.opcion = "Inicio"
    if st.sidebar.button("👥 Gestión de Usuarios"):
        st.session_state.opcion = "Gestion Usuarios"
    if st.sidebar.button("📋 Gestión de Tareas"):
        st.session_state.opcion = "Gestion Tareas"
    if st.sidebar.button("📊 Informes"):
        st.session_state.opcion = "Informes"
    if st.sidebar.button("📑 Reportes"):
        st.session_state.opcion = "Reportes"

    # Opción por defecto
    if 'opcion' not in st.session_state:
        st.session_state.opcion = "Inicio"

    # Controlador de las opciones seleccionadas
    if st.session_state.opcion == "Inicio":
        st.subheader("📖 Bienvenidos al Sistema de Gestión de Tareas")
        st.markdown("""
        Esta aplicación permite gestionar tareas asignadas a diferentes usuarios. Se pueden realizar las siguientes acciones:
        
        - **Gestión de Usuarios:** Crear, modificar y eliminar usuarios.
        - **Gestión de Tareas:** Crear, modificar, asignar y eliminar tareas, así como actualizar sus estados.
        
        ### 🔄 Pipeline del proyecto:
        1. Análisis y diseño de la solución.
        2. Definición de módulos y clases usando POO (Python).
        3. Implementación de funcionalidades con Streamlit para interactividad visual.
        4. Manejo de estado en sesión con `st.session_state`.

        ### ✒️ Autores:
        - **Ana María García Arias**
        - **Diana Gonzalez**
        """)
        
    elif st.session_state.opcion == "Gestion Usuarios":
        gestionar_usuarios()
    
    elif st.session_state.opcion == "Gestion Tareas":
        gestionar_tareas()
    
    elif st.session_state.opcion == "Informes":
        generar_informe()

    elif st.session_state.opcion == "Reportes":
        generar_reportes()

if __name__ == "__main__":
    main()
>>>>>>> c168e459545e6f4184de2ea5cc215662e2ed7e5d
