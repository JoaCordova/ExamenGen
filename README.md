# Custom Exam Generator
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-%23150458?logo=pandas)
![PyPDF2](https://img.shields.io/badge/PyPDF2-PDF%20handling-blueviolet)
![fpdf](https://img.shields.io/badge/fpdf-PDF%20Generator-brightgreen)

This Python script generates **30 unique, category-balanced exams** in PDF format from a bank of 45 questions (3 categories). Each student receives a different set of 30 questions with no duplicates.

For each student, the script also generates:
- A **PDF exam**
- A **PDF answer sheet**
- A **CSV file linking student IDs to correct answers**
## 📦 Installation
1. Prepare `preguntas.csv` with questions, options, correct answers, and categories  
2. Install dependencies:
```bash
pip install fpdf PyPDF2 pandas
 ```
## 🤖 Functionality
- Generates **30 exams**, one per student  
- Randomly selects questions per category  
- Ensures **no repeated questions within an exam**  
- Guarantees **unique exams** (at least 5 differences between students)  
- Uses **student IDs** as identifiers (e.g., 001, 002)  

## 📁 Output
- `examenes/examen_XXX.pdf` → individual exams  
- `answers_XXX.pdf` → answer sheet per student  
- `respuestas.csv` → answer key mapped to each student  
