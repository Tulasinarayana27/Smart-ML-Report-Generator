from fpdf import FPDF
from datetime import datetime
import os


def generate_pdf(data):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------------- Header ----------------

    pdf.set_fill_color(30, 90, 180)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 12, " SMART ML REPORT GENERATOR", 1, 1, "C", True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, "Machine Learning Analysis Report", 1, 1, "C")

    pdf.ln(5)

    # ---------------- Report Info ----------------

    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, "REPORT DETAILS", 1, 1, "L")

    pdf.set_font("Arial", "", 11)

    pdf.cell(60, 8, "Prepared For", 1)
    pdf.cell(130, 8, data["username"], 1, 1)

    pdf.cell(60, 8, "Dataset Name", 1)
    pdf.cell(130, 8, data["filename"], 1, 1)

    pdf.cell(60, 8, "Generated On", 1)
    pdf.cell(130, 8, datetime.now().strftime("%d-%m-%Y %I:%M %p"), 1, 1)

    pdf.ln(5)

    # ---------------- Dataset Summary ----------------

    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, "DATASET SUMMARY", 1, 1)

    pdf.set_font("Arial", "", 11)

    pdf.cell(60, 8, "Rows", 1)
    pdf.cell(130, 8, str(data["rows"]), 1, 1)

    pdf.cell(60, 8, "Columns", 1)
    pdf.cell(130, 8, str(data["columns"]), 1, 1)

    pdf.cell(60, 8, "Missing Values", 1)
    pdf.cell(130, 8, str(data["quality"]["missing"]), 1, 1)

    pdf.cell(60, 8, "Duplicate Rows", 1)
    pdf.cell(130, 8, str(data["quality"]["duplicates"]), 1, 1)

    pdf.cell(60, 8, "Dataset Quality", 1)
    pdf.cell(130, 8, str(data["quality"]["quality"]) + " / 100", 1, 1)

    pdf.ln(5)

    # ---------------- ML Result ----------------

    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, "MACHINE LEARNING RESULT", 1, 1)

    pdf.set_font("Arial", "", 11)

    pdf.cell(60, 8, "Best Model", 1)
    pdf.cell(130, 8, data["best_model"], 1, 1)

    pdf.cell(60, 8, "Accuracy", 1)
    pdf.cell(130, 8, str(data["best_accuracy"]) + " %", 1, 1)

    pdf.ln(5)

    # ---------------- Model Comparison ----------------

    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, "MODEL COMPARISON", 1, 1)

    pdf.set_font("Arial", "B", 11)

    pdf.cell(120, 8, "Model", 1, 0, "C")
    pdf.cell(70, 8, "Accuracy (%)", 1, 1, "C")

    pdf.set_font("Arial", "", 11)

    for model, accuracy in data["results"].items():
        pdf.cell(120, 8, model, 1)
        pdf.cell(70, 8, str(accuracy), 1, 1, "C")

    pdf.ln(10)

    # ---------------- Footer ----------------

    pdf.set_font("Arial", "I", 10)
    pdf.cell(
        190,
        8,
        "This report is generated automatically by Smart ML Report Generator.",
        0,
        1,
        "C",
    )

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f'{data["username"]}_ML_Report.pdf'
    filepath = os.path.join("reports", filename)

    pdf.output(filepath)

    return filepath