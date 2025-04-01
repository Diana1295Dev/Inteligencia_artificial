import streamlit as st
import pandas as pd
from io import BytesIO

# Función para convertir DataFrame a Excel y permitir descarga
def descargar_excel(df, nombre_archivo):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    st.download_button(
        label=f"📥 Descargar {nombre_archivo}.xlsx",
        data=processed_data,
        file_name=f"{nombre_archivo}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Genera reportes visuales
def generar_reportes():
    st.subheader("📑 Generador de Reportes")

    opcion_reporte = st.selectbox("Seleccione el tipo de reporte", ["Usuarios del sistema", "Tareas creadas"])

    if opcion_reporte == "Usuarios del sistema":
        if not st.session_state.usuarios:
            st.warning("⚠️ No hay usuarios registrados para mostrar.")
            return

        data_usuarios = [{
            'ID Usuario': user.usuario_id,
            'Nombre': user.nombre,
            'Correo Electrónico': user.correo,
            'Fecha Creación': user.fecha_creacion
        } for user in st.session_state.usuarios]

        df_usuarios = pd.DataFrame(data_usuarios)
        st.dataframe(df_usuarios)
        descargar_excel(df_usuarios, "Usuarios_Sistema")

    elif opcion_reporte == "Tareas creadas":
        if not st.session_state.tareas:
            st.warning("⚠️ No hay tareas creadas para mostrar.")
            return

        data_tareas = [{
            'ID Tarea': tarea.tarea_id,
            'Título': tarea.titulo,
            'Descripción': tarea.descripcion,
            'Responsable': tarea.responsable.nombre,
            'Fecha Creación': tarea.fecha_creacion,
            'Fecha Límite': tarea.fecha_limite,
            'Estado': tarea.estado
        } for tarea in st.session_state.tareas]

        df_tareas = pd.DataFrame(data_tareas)
        st.dataframe(df_tareas)
        descargar_excel(df_tareas, "Tareas_Creadas")
