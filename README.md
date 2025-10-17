🧠 Resume Ranker

A Flask-based web application that ranks resumes based on their keyword match with a given job description.
It automatically extracts text from uploaded resumes (.pdf, .docx, .txt) and compares them with the provided job description to calculate a match score and highlight common keywords.


---

🚀 Features

📁 Upload multiple resumes at once (PDF, DOCX, TXT)

🔍 Extract text automatically from resumes

⚖️ Compare each resume against a job description

📊 Rank resumes by their match percentage

💬 Display top 10 common keywords between each resume and job description

🌐 Simple and responsive web interface built using Flask + HTML/CSS



---

⚙️ Tech Stack

Backend: Python, Flask

Libraries Used:

PyPDF2 – for extracting text from PDFs

docx2txt – for reading DOCX files

os and flask – for handling uploads and requests

Frontend: HTML, CSS (through templates)



---

🧩 How It Works

1. The user uploads one or more resumes and enters a job description.


2. The app extracts text content from each resume file.


3. It compares words from the job description and each resume.


4. A score and match percentage are calculated based on common words.


5. Resumes are ranked and displayed in descending order of relevance.




---

📈 Output Example

Rank	Resume Name	Match %	Top Keywords

1	resume_1.pdf	78%	python, flask, api, sql, ml
2	resume_2.docx	62%	data, pandas, excel, analysis



---

💡 Future Improvements

Use TF-IDF or semantic similarity (BERT/SBERT) for smarter matching

Add download/export option for ranked results

Include skill extraction and weightage based scoring

Add user authentication for recruiters



---

🧑‍💻 Author

Naveen Kumar B

B.E. Computer Science (Data Science Specialization)
A passionate developer building practical, data-driven web applications.
