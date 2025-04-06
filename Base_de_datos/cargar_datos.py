import psycopg2
import pandas as pd
from urllib.parse import urlparse
import math

# ================== CONEXIÓN ==================
DATABASE_URL = "postgresql://postgres:caZQnWYDDpWxUBoZroiFnQMzfQifVghQ@hopper.proxy.rlwy.net:36834/railway"
url = urlparse(DATABASE_URL)

PGHOST = url.hostname
PGUSER = url.username
PGPASSWORD = url.password
PGDATABASE = url.path[1:]
PGPORT = url.port

# ================== CARGA DE DATOS ==================
df_agricultura_clean = pd.read_csv("agricultura_clean.csv")
df_clima = pd.read_csv("clima.csv")

df_agricultura_clean.columns = df_agricultura_clean.columns.str.strip()
df_clima.columns = df_clima.columns.str.strip()

# ================== CONEXIÓN A BASE DE DATOS ==================
try:
    connection = psycopg2.connect(
        host=PGHOST,
        user=PGUSER,
        password=PGPASSWORD,
        dbname=PGDATABASE,
        port=PGPORT
    )
    cursor = connection.cursor()
    print("✅ Conexión exitosa a PostgreSQL.")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    exit()

# ================== RECREAR TABLAS ==================
cursor.execute("""
    DROP TABLE IF EXISTS cultivos;
    CREATE TABLE cultivos (
        id SERIAL PRIMARY KEY,
        fecha INT,
        departamento VARCHAR(100),
        municipio VARCHAR(100),
        nombre_cultivo VARCHAR(100),
        periodo VARCHAR(50),
        area_sembrada REAL,
        area_cosechada REAL,
        produccion_ton REAL,
        rendimiento_t_ha REAL,
        ciclo VARCHAR(50)
    );
""")

cursor.execute("""
    DROP TABLE IF EXISTS clima;
    CREATE TABLE clima (
        id SERIAL PRIMARY KEY,
        fecha DATE,
        temperatura_max FLOAT,
        temperatura_min FLOAT,
        precipitacion FLOAT,
        temperatura_promedio FLOAT
    );
""")
connection.commit()

# ================== FUNCIONES DE CARGA ==================
def cargar_datos_agricultura(df):
    print("📥 Cargando datos de agricultura...")
    for index, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO cultivos (fecha, departamento, municipio, nombre_cultivo, periodo,
                                      area_sembrada, area_cosechada, produccion_ton, rendimiento_t_ha, ciclo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                int(row['fecha']),
                row['departamento'],
                row['municipio'],
                row['nombre_cultivo'],
                row['periodo'],
                float(row['area_sembrada']) if not math.isnan(row['area_sembrada']) else None,
                float(row['area_cosechada']) if not math.isnan(row['area_cosechada']) else None,
                float(row['produccion_ton']) if not math.isnan(row['produccion_ton']) else None,
                float(row['rendimiento_t_ha']) if not math.isnan(row['rendimiento_t_ha']) else None,
                row['ciclo']
            ))
        except Exception as e:
            print(f"⚠️ Error fila {index} agricultura: {e}")
            print("Datos problemáticos:", row.to_dict())
    connection.commit()
    print("✅ Datos de agricultura cargados.")

def cargar_datos_clima(df):
    print("📥 Cargando datos de clima...")
    for index, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO clima (fecha, temperatura_max, temperatura_min, precipitacion, temperatura_promedio)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                row['time'],
                row['temperature_2m_max'],
                row['temperature_2m_min'],
                row['precipitation_sum'],
                row['temperature_avg']
            ))
        except Exception as e:
            print(f"⚠️ Error fila {index} clima: {e}")
    connection.commit()
    print("✅ Datos de clima cargados.")

# ================== EJECUTAR CARGA ==================
cargar_datos_agricultura(df_agricultura_clean)
cargar_datos_clima(df_clima)

# ================== VERIFICAR CARGA ==================
print("\n🔎 Mostrando primeros registros:")

cursor.execute("SELECT * FROM cultivos LIMIT 5;")
for row in cursor.fetchall():
    print("🌾 Cultivo:", row)

cursor.execute("SELECT * FROM clima LIMIT 5;")
for row in cursor.fetchall():
    print("🌦️ Clima:", row)

# ================== CIERRE ==================
cursor.close()
connection.close()
print("🔒 Conexión cerrada.")