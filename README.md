# Generador de Exámenes Personalizados
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-%23150458?logo=pandas)
![PyPDF2](https://img.shields.io/badge/PyPDF2-PDF%20handling-blueviolet)
![fpdf](https://img.shields.io/badge/fpdf-PDF%20Generator-brightgreen)

![2025-05-13 18-55-08 (1)](https://github.com/user-attachments/assets/028b92ad-1bdf-47c5-b3d8-63b2dedb9d87)

Este script en Python genera exámenes en formato PDF para un grupo de 30 estudiantes, seleccionando aleatoriamente 30 preguntas a partir de un banco de 45 preguntas organizadas en tres categorías (15 por categoría). El objetivo es que cada prueba sea única para cada alumno. Además de los exámenes, el script adjunta un archivo de respuestas (answers.pdf) para cada uno y exporta un archivo CSV (respuestas.csv) con las claves correctas correspondientes a cada estudiante.

## 📦 Instalación
+ Antes de empezar, carga las preguntas, sus opciones, respuestas correctas y el tipo (categoría/tema) en `preguntas.csv`.   
+ Posteriormente, instala las librerías necesarias. Puedes hacerlo con `pip`:

```bash
pip install fpdf PyPDF2 pandas
```
+ Ejecuta el código.
## 🤖 Funcionamiento

Se generan 30 exámenes. Para cada alumno, se seleccionan aleatoriamente `n` preguntas por tema. Ninguna hoja tiene preguntas repetidas y cada examen tiene una combinación única de preguntas (al menos 5 diferentes entre ellos). El código del alumno se usa como identificador único (ej. 001, 002).
              
-   **Exportación de Archivos**:
    
    -   Cada examen se guarda como `examen_XXX.pdf` en la carpeta `examenes/`.
        
    -   Se crea el archivo `respuestas.csv` con todas las respuestas correctas por alumno.
