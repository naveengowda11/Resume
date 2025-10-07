import os
from flask import Flask, render_template, request
import docx2txt
import PyPDF2

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT"""
    if file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return ""


def calculate_match(resume_text, job_desc):
    """Calculate matching score and extract common keywords"""
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_desc.lower().split())

    common = resume_words & jd_words
    score = len(common)
    percentage = (score / len(jd_words)) * 100 if jd_words else 0

    return score, percentage, list(common)


@app.route("/", methods=["GET", "POST"])
def index():
    ranked_resumes = []

    if request.method == "POST":
        job_desc = request.form.get("job_desc", "").strip()
        files = request.files.getlist("resumes")

        if job_desc and files:
            for file in files:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                resume_text = extract_text(filepath)
                score, percentage, common_keywords = calculate_match(resume_text, job_desc)

                ranked_resumes.append({
                    "name": file.filename,
                    "score": score,
                    "percentage": round(percentage, 2),
                    "keywords": common_keywords[:10]  # top 10 matched keywords
                })

            # Sort by highest score
            ranked_resumes = sorted(ranked_resumes, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", ranked_resumes=ranked_resumes)


if __name__ == "__main__":
    app.run(debug=True)