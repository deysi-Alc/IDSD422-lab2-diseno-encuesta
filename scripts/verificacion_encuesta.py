# verificacion_encuesta.py — Auditoría de la encuesta (Python)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   python scripts/verificacion_encuesta.py

from pathlib import Path
import pandas as pd

# TODO 1: Cargar el CSV con pandas
ruta = (
    Path(__file__).resolve().parent.parent
    / "plantillas"
    / "encuesta_respuestas.csv"
)

df = pd.read_csv(ruta)

print("=== AUDITORÍA DE ENCUESTA ===")
print("Registros:", len(df))
print("Columnas:", len(df.columns))

# TODO 2: Mostrar los dtypes
print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)

# TODO 3: Mostrar los datos faltantes
print("\n=== DATOS FALTANTES ===")
print(df.isna().sum())

# TODO 4: Distribuciones generales
for columna in [
    "satisfaccion_general",
    "recomendaria"
]:
    print(f"\n=== {columna} ===")
    print(
        df[columna].value_counts(
            dropna=False
        ).sort_index()
    )

# Separar las respuestas reales de las simuladas
if "origen" in df.columns:
    reales = df.loc[
        df["origen"].astype(str).str.lower()
        == "real"
    ].copy()

    simuladas = df.loc[
        df["origen"].astype(str).str.lower()
        == "simulada"
    ].copy()

    print("\n=== ORIGEN DE LOS DATOS ===")
    print("Reales:", len(reales))
    print("Simuladas:", len(simuladas))
else:
    raise ValueError(
        "El CSV debe contener la columna origen"
    )

# Auditoría únicamente de registros reales
print("\n=== ANÁLISIS DE RESPUESTAS REALES ===")

if reales.empty:
    print("Aún no existen respuestas reales.")
else:
    for columna in [
        "satisfaccion_general",
        "recomendaria"
    ]:
        print(f"\n{columna}:")
        print(
            reales[columna].value_counts(
                dropna=False
            ).sort_index()
        )

    print("\nFaltantes en registros reales:")
    print(reales.isna().sum())

    print("\nPorcentaje de recomendación:")
    recomendacion = (
        reales["recomendaria"].eq("Si").mean()
        * 100
    )
    print(f"{recomendacion:.2f}%")

    print("\nSatisfacción favorable (4 o 5):")
    validas = pd.to_numeric(
        reales["satisfaccion_general"],
        errors="coerce"
    ).dropna()

    if len(validas) > 0:
        porcentaje = validas.ge(4).mean() * 100
        print(f"{porcentaje:.2f}%")
    else:
        print("Sin puntuaciones válidas")

    # Revisión de variables adicionales
    for columna in [
        "frecuencia_visita",
        "interes_programa",
        "beneficio_preferido",
        "aspecto_mejora"
    ]:
        if columna in reales.columns:
            print(f"\nDistribución de {columna}:")
            print(
                reales[columna].value_counts(
                    dropna=False
                )
            )

    # Comprobaciones de validez
    if "edad" in reales.columns:
        edad = pd.to_numeric(
            reales["edad"],
            errors="coerce"
        )
        print(
            "\nEdades inválidas:",
            (edad.lt(18) | edad.isna()).sum()
        )

    for columna in [
        "satisfaccion_general",
        "interes_programa"
    ]:
        if columna in reales.columns:
            valores = pd.to_numeric(
                reales[columna],
                errors="coerce"
            )
            invalidos = (
                ~valores.isin([1, 2, 3, 4, 5])
            ).sum()
            print(
                f"Valores inválidos en {columna}:",
                invalidos
            )

    # Posibles señales de sesgo
    print("\n=== INTERPRETACIÓN PRELIMINAR ===")
    print(
        "Una concentración de participantes "
        "en una sola categoría puede indicar "
        "un problema de cobertura."
    )
    print(
        "Una concentración extrema de "
        "respuestas positivas requiere "
        "revisar un posible sesgo de respuesta."
    )
    print(
        "El sesgo de no respuesta necesita "
        "también el registro de invitaciones "
        "y rechazos."
    )
