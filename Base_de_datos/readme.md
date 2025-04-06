# 🌱 Inteligencia Artificial - Dashboard Agricultura y Clima

Este proyecto forma parte de un repositorio dedicado a aprender sobre Inteligencia Artificial. En esta sección se centra en visualizar datos agrícolas y climáticos de Colombia usando **Streamlit** y **PostgreSQL**.

## 📊 ¿Qué hace este proyecto?

- Visualiza datos de cultivos (área sembrada, cosechada, producción, rendimiento).
- Muestra información climática (temperaturas máximas, mínimas, promedio y precipitación).
- Se conecta a una base de datos remota (Railway con PostgreSQL).
- Interfaz amigable y simple hecha con Streamlit.

## 🚀 Cómo ejecutar localmente

1. Clona este repositorio:

```bash
git clone https://github.com/Diana1295Dev/Inteligencia_artificial.git
cd Inteligencia_artificial
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
streamlit run app.py
```

## 📦 Requisitos

Este proyecto usa las siguientes bibliotecas (incluidas en `requirements.txt`):

- streamlit  
- pandas  
- psycopg2-binary  

## 💄 Estructura del proyecto

```
Inteligencia_artificial/
│
├── app.py                <- Código de la interfaz con Streamlit
├── cargar_datos.py       <- Carga datos a PostgreSQL
├── procesar_datos.py     <- Limpieza y preprocesamiento de datos
├── requirements.txt      <- Lista de dependencias
├── README.md             <- Este archivo
└── (archivos CSV)        <- Datos procesados y limpios
```

## 📌 Notas

- Asegúrate de que tu conexión PostgreSQL esté correctamente configurada con variables de entorno o directamente en el código (`DATABASE_URL`).
- Puedes subir este proyecto a Streamlit Cloud o a cualquier servidor con Python.

