from flask import Flask, render_template, request, send_file
import os
import pandas as pd

from preprocessing import preprocess_dataset
from ml_models import train_models
from dataset_quality import calculate_dataset_quality
from report_generator import generate_pdf


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER


# Store latest report data
report_data = {}
# Store latest report data
report_data = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report", methods=["POST"])
def report():

    global report_data

    username = request.form["username"]
    dataset = request.files["dataset"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], dataset.filename)
    dataset.save(filepath)

    df = pd.read_csv(filepath)

    df = preprocess_dataset(df)

    rows = df.shape[0]
    columns = df.shape[1]

    quality = calculate_dataset_quality(df)

    best_model, best_accuracy, results = train_models(df)

    # Save data for PDF generation
    report_data = {
        "username": username,
        "filename": dataset.filename,
        "rows": rows,
        "columns": columns,
        "best_model": best_model,
        "best_accuracy": best_accuracy,
        "results": results,
        "quality": quality
    }

    return render_template(
        "report.html",
        username=username,
        filename=dataset.filename,
        rows=rows,
        columns=columns,
        best_model=best_model,
        best_accuracy=best_accuracy,
        results=results,
        quality=quality
    )


@app.route("/download")
def download():

    pdf_path = generate_pdf(report_data)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)