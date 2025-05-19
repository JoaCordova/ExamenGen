import pandas as pd

# Configuración
num_temas = 3
preguntas_por_tema = 10
total_preguntas = num_temas * preguntas_por_tema

# Leer archivos
try:
    alumnos_df = pd.read_csv("respuestas_alumnos.csv")
    respuestas_correctas_df = pd.read_csv("respuestas_correctas.csv")
except Exception as e:
    print(f"Error al leer archivos: {e}")
    exit()

# Lista de resultados
resultados = []

for index, row in alumnos_df.iterrows():
    codigo = row['codigo']
    nombre = row['nombre']
    respuestas_alumno = [str(r) if pd.notna(r) else "-" for r in row[1:-1]]

    # Obtener respuestas correctas
    fila_correcta = respuestas_correctas_df[respuestas_correctas_df['codigo'] == codigo]
    if fila_correcta.empty:
        print(f"⚠️ Sin respuestas correctas para el código {codigo}")
        continue
    respuestas_correctas = [str(r) if pd.notna(r) else "-" for r in fila_correcta.iloc[0, 1:]]

    # Evaluar respuestas
    puntajes_por_pregunta = [1 if r_a == r_c else 0 for r_a, r_c in zip(respuestas_alumno, respuestas_correctas)]
    puntaje_total = sum(puntajes_por_pregunta)
    nota_final = round(puntaje_total / 3, 1)

    # Crear fila
    resultado = {
        "codigo": codigo,
        "nombre": nombre,
        "puntaje_total": puntaje_total,
        "nota_final_10": nota_final
    }

    # Añadir columnas por pregunta (P1, P2, ..., P30)
    for i in range(total_preguntas):
        resultado[f"P{i+1}"] = puntajes_por_pregunta[i]

    resultados.append(resultado)

# Guardar como CSV
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("puntajes_detallados.csv", index=False)
print("✅ Archivo 'puntajes_detallados.csv' generado correctamente.")
