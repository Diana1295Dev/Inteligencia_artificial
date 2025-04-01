# 📝 Sistema de Gestión de Tareas con Streamlit

Este proyecto es un sistema interactivo desarrollado con **Python** usando el framework **Streamlit**, enfocado en gestionar tareas asignadas a usuarios de una manera sencilla y visual.

## 📌 Funcionalidades Principales

- **Gestión de Usuarios:**
  - Crear, modificar y eliminar usuarios.

- **Gestión de Tareas:**
  - Crear, modificar, asignar, eliminar tareas, y gestionar estados (Pendiente, En Progreso, Completada).

- **Informes y Reportes:**
  - Gráficos interactivos sobre tareas por estado.
  - Reportes exportables en Excel para usuarios y tareas.

## 🚧 Estructura del Proyecto

```
GestorTareas/
├── app.py                 # Punto de entrada principal (Streamlit)
├── requirements.txt       # Dependencias del proyecto
├── modulos/               # Clases principales (POO)
│   ├── Usuario.py
│   ├── Tarea.py
│   ├── Estado.py
│   ├── Historial.py
│   ├── informes.py
│   └── reportes.py
└── env/                   # Entorno virtual de Python
```

## ⚙️ Tecnologías Utilizadas

- Python (POO)
- Streamlit
- Pandas
- Numpy
- xlsxwriter (exportar a Excel)

## 💻 Instalación y uso local

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/<nombre-repo>.git
cd <nombre-repo>
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv env

# Activar el entorno
# Windows
.\env\Scripts\activate

# Linux/Mac
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente una pestaña en tu navegador: `http://localhost:8501`

## 🚀 Deploy en Streamlit Cloud

1. **Subir a GitHub:**
   - Crea un repositorio en GitHub y sube todo tu proyecto.

2. **Despliegue en Streamlit Cloud:**
   - Ve a [Streamlit Cloud](https://streamlit.io/cloud).
   - Conecta tu cuenta con GitHub.
   - Haz clic en **New app** y selecciona tu repositorio.
   - Indica `app.py` como archivo principal y da clic en **Deploy**.

¡Tu aplicación estará lista para usarse en unos minutos!

## ✨ Autoras

- Ana María García Arias
- Diana Gonzalez