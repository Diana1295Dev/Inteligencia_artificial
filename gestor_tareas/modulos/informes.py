import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Genera el informe visual y tabla resumen
def generar_informe():
    st.subheader("📊 Informe de Tareas por Estado")

    if not st.session_state.tareas:
        st.warning("⚠️ No hay tareas registradas para generar informe.")
        return

    # Crear DataFrame con las tareas
    tareas_data = [{
        'Tarea': tarea.titulo,
        'Usuario': tarea.responsable.nombre,
        'Estado': tarea.estado
    } for tarea in st.session_state.tareas]

    df = pd.DataFrame(tareas_data)

    # Filtro por usuario
    usuarios_disponibles = ['Todos'] + df['Usuario'].unique().tolist()
    usuario_seleccionado = st.selectbox("Filtrar por usuario", usuarios_disponibles)

    if usuario_seleccionado != 'Todos':
        df = df[df['Usuario'] == usuario_seleccionado]

    # Gráfica: Cantidad de tareas por estado
    conteo_estados = df['Estado'].value_counts()

    fig, ax = plt.subplots()
    conteo_estados.plot(kind='bar', ax=ax)
    ax.set_xlabel('Estado')
    ax.set_ylabel('Cantidad de Tareas')
    ax.set_title('Cantidad de Tareas por Estado')

    st.pyplot(fig)

    # Tabla resumen
    st.subheader("📋 Tabla Resumen")
    resumen = df.groupby(['Tarea', 'Usuario', 'Estado']).size().reset_index(name='Cantidad')
    st.dataframe(resumen)