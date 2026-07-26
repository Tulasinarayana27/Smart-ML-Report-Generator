from flask import Flask, render_template, request, send_file
import os
import pandas as pd

from preprocessing import preprocess_dataset
from ml_models import train_models
from dataset_quality import calculate_dataset_quality
from report_generator import generate_pdf


app = Flask(__name__)


# -------------------------------
# Folder Configuration
# -------------------------------

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER


# Store latest report data
report_data = {}


# -------------------------------
# Home Page
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")



# -------------------------------
# Generate Report
# -------------------------------

@app.route("/report", methods=["POST"])
def report():

    global report_data

    try:

        # Get username
        username = request.form.get("username")

        # Get uploaded file
        dataset = request.files.get("dataset")


        if dataset is None:
            return "No dataset uploaded"


        # Save uploaded dataset
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            dataset.filename
        )

        dataset.save(filepath)



        # Read CSV
        df = pd.read_csv(filepath)


        # Limit dataset size for Render free server
        if len(df) > 10000:
            df = df.sample(
                10000,
                random_state=42
            )


        # Data preprocessing
        df = preprocess_dataset(df)


        rows = df.shape[0]
        columns = df.shape[1]


        # Dataset quality analysis
        quality = calculate_dataset_quality(df)


        # Train ML models
        best_model, best_accuracy, results = train_models(df)



        # Store report information
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


    except Exception as e:

        print("ERROR:", e)

        return f"""
        <h2>Error occurred</h2>
        <p>{str(e)}</p>
        """




# -------------------------------
# Download PDF
# -------------------------------

@app.route("/download")
def download():

    try:

        pdf_path = generate_pdf(report_data)

        return send_file(
            pdf_path,
            as_attachment=True
        )

    except Exception as e:

        return f"PDF Error: {str(e)}"




# -------------------------------
# Local Run
# -------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )