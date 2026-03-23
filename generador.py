import csv
import random
import os
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd

# Inputs
exam_title = input("Enter the exam title: ")
course_name = input("Enter the course name: ")
exam_date = input("Enter the exam date (e.g. 18/June/2000): ")

# PDF class
class ExamPDF(FPDF):
    def __init__(self, student_code):
        super().__init__()
        self.student_code = student_code

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Code: {self.student_code}", align="C")

# Load CSV
dataframe = pd.read_csv("questions.csv")
dataframe["Type"] = dataframe["Type"].str.strip().str.lower()

topics = dataframe["Type"].unique()

# Load questions by topic
def load_questions(df, topic):
    question_list = []
    for _, row in df[df["Type"] == topic].iterrows():
        question_list.append({
            "text": row["Pregunta"],
            "options": [
                row["Option A"],
                row["Option B"],
                row["Option C"],
                row["Option D"],
                row["Option E"],
            ],
            "answer": row["Correct answer"].strip().upper()
        })
    return question_list

# Question bank
question_bank = {topic: load_questions(dataframe, topic) for topic in topics}

# Parameters
num_students = 30
questions_per_topic = 10

# Generate unique exams
used_combinations = set()
exam_versions = []

for i in range(1, num_students + 1):
    student_code = f"{i:03d}"
    while True:
        selected_questions = {
            topic: random.sample(question_bank[topic], questions_per_topic)
            for topic in topics
        }
        combo_key = tuple(sorted(q["text"] for group in selected_questions.values() for q in group))
        
        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            break

    exam_versions.append({
        "code": student_code,
        "sections": selected_questions
    })

# Generate exam PDF
def generate_exam_pdf(exam):
    pdf = ExamPDF(exam["code"])
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, exam_title, ln=1, align="C")
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"Name: __________  Course: {course_name}  Date: {exam_date}", ln=1)

    for topic, questions in exam["sections"].items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, topic.upper(), ln=1)
        
        pdf.set_font("Arial", '', 11)
        for index, question in enumerate(questions, 1):
            pdf.multi_cell(0, 6, f"{index}. {question['text']}")
            for option in question["options"]:
                pdf.cell(0, 6, f"   {option}", ln=1)
            pdf.ln(2)

    return pdf

# Footer creation
def create_footer_page(student_code):
    footer_pdf = FPDF()
    footer_pdf.add_page()
    footer_pdf.set_font("Arial", "I", 10)
    footer_pdf.set_y(-15)
    footer_pdf.cell(0, 10, f"Code: {student_code}", align="C")
    
    temp_path = "footer_temp.pdf"
    footer_pdf.output(temp_path)
    
    reader = PdfReader(temp_path)
    footer_page = reader.pages[0]
    
    os.remove(temp_path)
    return footer_page

def add_footer_to_answers(input_path, student_code, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    footer_page = create_footer_page(student_code)

    for page in reader.pages:
        page.merge_page(footer_page)
        writer.add_page(page)

    with open(output_path, "wb") as file:
        writer.write(file)

# Generate PDFs
os.makedirs("exams", exist_ok=True)

for exam in exam_versions:
    code = exam["code"]
    
    pdf = generate_exam_pdf(exam)
    temp_exam_path = f"exams/temp_{code}.pdf"
    pdf.output(temp_exam_path)

    answers_with_footer_path = f"exams/answers_{code}.pdf"
    add_footer_to_answers("answers.pdf", code, answers_with_footer_path)

    writer = PdfWriter()
    writer.append(PdfReader(temp_exam_path))
    writer.append(PdfReader(answers_with_footer_path))

    final_path = f"exams/exam_{code}.pdf"
    with open(final_path, "wb") as file:
        writer.write(file)

    os.remove(temp_exam_path)
    os.remove(answers_with_footer_path)

# Generate answers CSV
with open("answers_output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    headers = ["Code"] + [f"Q{i+1}" for i in range(questions_per_topic * len(topics))]
    writer.writerow(headers)

    for exam in exam_versions:
        row = [exam["code"]]
        for topic in topics:
            row += [q["answer"] for q in exam["sections"][topic]]
        writer.writerow(row)

print("✔️ Exams generated and answers exported.")
