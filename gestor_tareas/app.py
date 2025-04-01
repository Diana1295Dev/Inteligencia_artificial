import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modulos')))

import streamlit as st
from datetime import datetime
from Usuario import Usuario
from Tarea import Tarea
from Estado import Estado
from informes import generar_informe
from reportes import generar_reportes



# Inicializar variables persistentes usando st.session_state
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = []
if 'contador_id' not in st.session_state:
    st.session_state.contador_id = 1

if 'tareas' not in st.session_state:
    st.session_state.tareas = []
if 'contador_tarea_id' not in st.session_state:
    st.session_state.contador_tarea_id = 1


def gestionar_usuarios():
    st.subheader("👥 Gestión de Usuarios")

    # Inicializar campos en session_state
    if 'nombre_usuario' not in st.session_state:
        st.session_state.nombre_usuario = ""
    if 'correo_usuario' not in st.session_state:
        st.session_state.correo_usuario = ""

    # Formulario para agregar usuario
    with st.form("Agregar Usuario"):
        nombre_usuario = st.text_input("Nombre del Usuario", value=st.session_state.nombre_usuario)
        correo_usuario = st.text_input("Correo Electrónico", value=st.session_state.correo_usuario)
        submit_button = st.form_submit_button("Agregar Usuario")

        if submit_button:
            if not nombre_usuario.strip() or not correo_usuario.strip():
                st.error("❗ El nombre y el correo electrónico no pueden estar vacíos.")
            elif any(user.nombre == nombre_usuario or user.correo == correo_usuario for user in st.session_state.usuarios):
                st.warning("⚠️ Usuario ya existe.")
            else:
                fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                nuevo_usuario = Usuario(st.session_state.contador_id, nombre_usuario, correo_usuario, fecha_creacion)
                st.session_state.usuarios.append(nuevo_usuario)
                st.success(f"✅ Usuario '{nombre_usuario}' agregado exitosamente con ID: {st.session_state.contador_id}")
                st.session_state.contador_id += 1

                # Limpiar los campos después de agregar
                st.session_state.nombre_usuario = ""
                st.session_state.correo_usuario = ""

                # Mostrar solo el último usuario agregado
                st.subheader("🆕 Último Usuario Creado")
                st.markdown(f"""
                ---
                **🆔 ID:** {nuevo_usuario.usuario_id}  
                **👤 Nombre:** {nuevo_usuario.nombre}  
                **📧 Correo Electrónico:** {nuevo_usuario.correo}  
                **🗓️ Fecha Creación:** {nuevo_usuario.fecha_creacion}
                """)

    # Opciones para Modificar y Eliminar usuarios solo si hay usuarios creados
    if st.session_state.usuarios:
        st.subheader("✏️ Modificar Usuario")
        usuario_modificar = st.selectbox("Selecciona usuario para modificar", [f"{u.usuario_id} - {u.nombre}" for u in st.session_state.usuarios])
        usuario_seleccionado = next((u for u in st.session_state.usuarios if u.usuario_id == int(usuario_modificar.split(" - ")[0])), None)

        if usuario_seleccionado:
            nuevo_nombre = st.text_input("Nuevo nombre", usuario_seleccionado.nombre)
            nuevo_correo = st.text_input("Nuevo correo electrónico", usuario_seleccionado.correo)
            if st.button("Actualizar Usuario"):
                usuario_seleccionado.nombre = nuevo_nombre
                usuario_seleccionado.correo = nuevo_correo
                st.success("🔄 Usuario actualizado exitosamente.")

        st.subheader("🗑️ Eliminar Usuario")
        usuario_eliminar = st.selectbox("Selecciona usuario para eliminar", [f"{u.usuario_id} - {u.nombre}" for u in st.session_state.usuarios])
        if st.button("Eliminar Usuario"):
            usuario_id_a_eliminar = int(usuario_eliminar.split(" - ")[0])
            st.session_state.usuarios = [u for u in st.session_state.usuarios if u.usuario_id != usuario_id_a_eliminar]
            st.success("🗑️ Usuario eliminado exitosamente.")


def gestionar_tareas():
    st.subheader("📌 Gestión de Tareas")

    if not st.session_state.usuarios:
        st.warning("⚠️ Primero registra usuarios para asignarles tareas.")
        return

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