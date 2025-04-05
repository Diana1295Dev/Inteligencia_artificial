import pandas as pd
import requests

# ================== AGRICULTURA ==================
url_agricultura = "https://www.datos.gov.co/resource/7475-g9fq.csv"
df_agricultura = pd.read_csv(url_agricultura)

# Renombrar columnas
df_agricultura_clean = df_agricultura.rename(columns={
    'a_o': 'fecha',
    '_cultivo_': 'nombre_cultivo',
    '_rea_sembrada_ha_': 'area_sembrada',
    '_rea_cosechada_ha_': 'area_cosechada',
    'producci_n_ton': 'produccion_ton',
    'rendimiento_t_ha_': 'rendimiento_t_ha'
})

# Limpiar textos y limitar longitud
for col in ['departamento', 'municipio', 'nombre_cultivo']:
    df_agricultura_clean[col] = df_agricultura_clean[col].astype(str).str.strip().str[:100]

# Convertir columnas numéricas
cols_numericas = ['area_sembrada', 'area_cosechada', 'produccion_ton', 'rendimiento_t_ha']
for col in cols_numericas:
    df_agricultura_clean[col] = pd.to_numeric(df_agricultura_clean[col], errors='coerce')

# Asegurarse que la columna 'fecha' sea tipo entero (año)
df_agricultura_clean['fecha'] = pd.to_numeric(df_agricultura_clean['fecha'], errors='coerce').astype('Int64')

# Guardar archivo limpio
df_agricultura_clean.to_csv("agricultura_clean.csv", index=False)

# ================== CLIMA ==================
url_clima = "https://api.open-meteo.com/v1/forecast"
params = {
    'latitude': 5.4444,
    'longitude': -72.3914,
    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
    'timezone': 'America/Bogota'
}

response = requests.get(url_clima, params=params)
if response.status_code == 200:
    clima_data = response.json()
    df_clima = pd.DataFrame(clima_data['daily'])

    df_clima['time'] = pd.to_datetime(df_clima['time'])
    df_clima['temperature_avg'] = (
        df_clima['temperature_2m_max'] + df_clima['temperature_2m_min']
    ) / 2

    df_clima.to_csv("clima.csv", index=False)
    print("✅ Datos de clima guardados correctamente.")
else:
    print("❌ Error al obtener datos de clima.")

# ================== MOSTRAR LOS DATAFRAMES ==================
print("\n📊 Primeras filas del DataFrame de Agricultura:")
print(df_agricultura_clean.head())

print("\n🌦️ Primeras filas del DataFrame de Clima:")
print(df_clima.head())
