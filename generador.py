import csv
import random
import os
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd

#  Inputs 
titulo_examen = input("Introduce el título del examen: ")
curso = input("Introduce el curso: ")
fecha_examen  = input("Introduce la fecha (ej. 18/junio/2000): ")

#  PDF footer 
class PDF(FPDF):
    def __init__(self, codigo_alumno):
        super().__init__()
        self.codigo = codigo_alumno

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Código: {self.codigo}", align="C")

#  Cargar CSV y detectar temas 
df = pd.read_csv("preguntas.csv")
df["Tipo"] = df["Tipo"].str.strip().str.lower()

temas = df["Tipo"].unique()  # Lista de tipos únicos (bloques)

# Cargar preguntas por tema
def cargar_preguntas(df, tipo):
    preguntas = []
    for _, row in df[df["Tipo"] == tipo].iterrows():
        preguntas.append({
            "texto": row["Pregunta"],
            "opciones": [
                row["Opción A"],
                row["Opción B"],
                row["Opción C"],
                row["Opción D"],
                row["Opción E"],
            ],
            "respuesta": row["Respuesta Correcta"].strip().upper()
        })
    return preguntas

#  Generar banco por tema 
banco = {tema: cargar_preguntas(df, tema) for tema in temas}

# Parámetros
alumnos = 30
por_tema = 10

#  Crear combinaciones únicas por alumno 
usadas = set()
pruebas = []

for n in range(1, alumnos + 1):
    codigo = f"{n:03d}"
    while True:
        seleccion = {tema: random.sample(banco[tema], por_tema) for tema in temas}
        combo = tuple(sorted(q["texto"] for lista in seleccion.values() for q in lista))
        if combo not in usadas:
            usadas.add(combo)
            break
    pruebas.append({
        "codigo": codigo,
        "bloques": seleccion  # dict con claves = tema
    })

#  Generar examen en PDF 
def generar_examen(prueba):
    pdf = PDF(prueba["codigo"])
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, titulo_examen, ln=1, align="C")
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"Nombre: __________  Curso: {curso}  Fecha: {fecha_examen}", ln=1)

    for tema, preguntas in prueba["bloques"].items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, tema.upper(), ln=1)
        pdf.set_font("Arial", '', 11)
        for i, pregunta in enumerate(preguntas, 1):
            pdf.multi_cell(0, 6, f"{i}. {pregunta['texto']}")
            for op in pregunta["opciones"]:
                pdf.cell(0, 6, f"   {op}", ln=1)
            pdf.ln(2)
    return pdf

#  Footer para answers.pdf 
def create_footer_pdf(codigo_alumno):
    footer_pdf = FPDF()
    footer_pdf.add_page()
    footer_pdf.set_font("Arial", "I", 10)
    footer_pdf.set_y(-15)
    footer_pdf.cell(0, 10, f"Código: {codigo_alumno}", align="C")
    
    footer_path = "footer_temp.pdf"
    footer_pdf.output(footer_path)
    
    footer_reader = PdfReader(footer_path)
    footer_page = footer_reader.pages[0]
    
    os.remove(footer_path)
    return footer_page

def add_footer_to_answers_pdf(answers_path, codigo_alumno, output_path):
    reader = PdfReader(answers_path)
    writer = PdfWriter()
    footer = create_footer_pdf(codigo_alumno)

    for page in reader.pages:
        page.merge_page(footer)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

#  Generar PDFs combinados 
os.makedirs("examenes", exist_ok=True)

for pr in pruebas:
    codigo = pr["codigo"]
    pdf = generar_examen(pr)
    examen_temp = f"examenes/temp_{codigo}.pdf"
    pdf.output(examen_temp)

    answers_with_footer = f"examenes/answers_{codigo}.pdf"
    add_footer_to_answers_pdf("answers.pdf", codigo, answers_with_footer)

    merger = PdfWriter()
    merger.append(PdfReader(examen_temp))
    merger.append(PdfReader(answers_with_footer))

    with open(f"examenes/examen_{codigo}.pdf", "wb") as f:
        merger.write(f)

    os.remove(examen_temp)
    os.remove(answers_with_footer)

#  Generar archivo CSV de respuestas 
with open("respuestas.csv", "w", newline="") as f:
    wr = csv.writer(f)
    headers = ["Código"] + [f"P{i+1}" for i in range(por_tema * len(temas))]
    wr.writerow(headers)

    for pr in pruebas:
        fila = [pr["codigo"]]
        for tema in temas:
            fila += [q["respuesta"] for q in pr["bloques"][tema]]
        wr.writerow(fila)

print("✔️ Exámenes generados con títulos desde el CSV y respuestas exportadas.")
