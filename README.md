# Generador de Exámenes Personalizados

Este script en Python genera exámenes PDF para un número determinado de estudiantes, usando un banco de preguntas categorizado. También adjunta un archivo de respuestas (`answers.pdf`) a cada examen y exporta un archivo `respuestas.csv` con las claves correctas para cada alumno.


# Entradas principales

-   **Archivo `preguntas.csv`**: Contiene las preguntas, sus opciones, respuestas correctas y el tipo (categoría/tema).
    
-   **Archivo `answers.pdf`**: Documento general con respuestas que se adjunta a cada examen individual.
    
-   **Inputs del usuario**:
    
    -   Título del examen (`titulo_examen`)
        
    -   Fecha del examen (`fecha_examen`)

## Funcionamiento

-   **Carga del Banco de Preguntas**:
    
    -   Se lee `preguntas.csv` usando `pandas`.
        
    -   Se detectan automáticamente todos los temas únicos (como `"historia de la imprenta"`, `"puntuación"`, etc.).
        
    -   Se agrupan las preguntas por tema en un diccionario `banco`.
        
-   **Generación de Exámenes**:
    
    -   Se genera un número determinado de exámenes (por defecto, 30).
        
    -   Para cada alumno, se seleccionan aleatoriamente `n` preguntas por tema.
        
    -   Se garantiza que ninguna hoja tenga preguntas repetidas y que cada examen tenga una combinación única de preguntas (al menos 5 diferentes entre ellos).
        
    -   El código del alumno se usa como identificador único (ej. `001`, `002`, ...).
        
-   **Creación del PDF del Examen**:
    
    -   Se usa `fpdf` para crear el examen con el título, fecha y bloques por tema.
        
    -   Se inserta un pie de página (footer) en cada hoja con el código del alumno.
        
-   **Unión con `answers.pdf`**:
    
    -   El PDF de respuestas se copia y se le añade el mismo pie de página personalizado.
        
    -   Se combinan ambos archivos (`examen + respuestas`) con `PyPDF2`.
        
-   **Exportación de Archivos**:
    
    -   Cada examen se guarda como `examen_XXX.pdf` en la carpeta `examenes/`.
        
    -   Se crea el archivo `respuestas.csv` con todas las respuestas correctas por alumno.

## 📁 Estructura de Archivos del Proyecto
```
📦 generador_examenes/
├── generador.py # Script principal
├── preguntas.csv # Banco de preguntas (entrada)
├── answers.pdf # Archivo de respuestas adjunto a cada examen
├── respuestas.csv # Claves de respuestas correctas por alumno (salida)
├── examenes/ # Carpeta de salida con los exámenes generados
│ ├── examen_001.pdf
│ ├── examen_002.pdf
│ └── ...
```
