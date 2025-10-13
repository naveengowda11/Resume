import os
from flask import Flask, render_template, request, send_file
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- Full IT Skills Keywords ----------------
KEYWORDS = set([k.lower() for k in [
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "HTML", "CSS",
    "Bootstrap", "Tailwind CSS", "React", "React.js", "Next.js", "Angular", "Vue.js",
    "Node.js", "Express.js", "Flask", "FastAPI", "Django", "Spring", "Spring Boot",
    "Kotlin", "Swift", "Objective-C", "PHP", "Ruby", "Go", "Rust", "SQL", "MySQL",
    "PostgreSQL", "SQLite", "MongoDB", "Firebase", "NoSQL", "Oracle", "Redis", "Elasticsearch",
    "GraphQL", "REST API", "Microservices", "OOP", "Object Oriented Programming",
    "Functional Programming", "DSA", "Data Structures", "Algorithms", "System Design",
    "Design Patterns", "Software Development Life Cycle", "SDLC", "Agile", "Scrum",
    "Kanban", "Version Control", "Git", "GitHub", "GitLab", "Bitbucket", "CI/CD",
    "Jenkins", "Docker", "Kubernetes", "Terraform", "Ansible", "AWS", "Amazon Web Services",
    "Azure", "Google Cloud Platform", "GCP", "Cloud Computing", "Cloud Deployment",
    "Serverless", "Lambda", "API Development", "Authentication", "Authorization",
    "OAuth", "JWT", "Unit Testing", "Integration Testing", "Automation Testing", "Pytest",
    "Selenium", "Postman", "Insomnia", "JIRA", "Confluence", "Trello", "Slack", "VS Code",
    "Eclipse", "IntelliJ", "PyCharm", "NetBeans", "Xcode", "Android Studio", "Firebase",
    "Figma", "UI/UX", "User Interface", "User Experience", "Wireframing", "Prototyping",
    "Responsive Design", "WebSockets", "Caching", "Load Balancing", "Performance Optimization",
    "Debugging", "Troubleshooting", "Deployment", "Production Environment", "Containerization",
    "Virtualization", "Linux", "Unix", "Windows Server", "Shell Scripting", "Bash",
    "PowerShell", "Command Line", "API Integration", "Third-Party APIs", "Webhooks",
    "Data Analysis", "Data Visualization", "NumPy", "Pandas", "Matplotlib", "Seaborn",
    "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "NLP", "Natural Language Processing",
    "Deep Learning", "Machine Learning", "Artificial Intelligence", "Model Training",
    "Model Evaluation", "Feature Engineering", "Big Data", "Apache Spark", "Hadoop",
    "ETL", "Pipeline", "Data Cleaning", "Data Wrangling", "SQL Queries", "Stored Procedures",
    "Indexing", "Joins", "Database Management", "Database Design", "Data Mining",
    "Data Warehousing", "Power BI", "Tableau", "Excel", "Statistics", "Probability",
    "Regression", "Classification", "Clustering", "Time Series", "Reinforcement Learning",
    "Computer Vision", "Image Processing", "OpenCV", "TensorFlow Lite", "ONNX", "MLOps",
    "DevOps", "Monitoring", "Logging", "Prometheus", "Grafana", "ELK Stack", "Security",
    "Penetration Testing", "Vulnerability Assessment", "Encryption", "Cryptography",
    "Network Security", "Ethical Hacking", "Firewall", "VPN", "DNS", "TCP/IP", "HTTP",
    "HTTPS", "SSL", "TLS", "Frontend", "Backend", "Full Stack", "API Gateway", "Scalability",
    "Load Testing", "Unit Tests", "Code Review", "Code Optimization", "Version Control System",
    "Test Cases", "Bug Fixing", "Code Refactoring", "Software Architecture",
    "Continuous Integration", "Continuous Deployment", "Team Collaboration", "Problem Solving",
    "Analytical Thinking", "Leadership", "Communication Skills", "Project Management",
    "Time Management", "Adaptability", "Critical Thinking", "Innovation", "Creativity",
    "Research", "Collaboration", "Mentorship", "Documentation", "Requirement Analysis",
    "Software Testing", "Automation", "Debugging Tools", "IDE", "Build Systems",
    "Package Management", "npm", "yarn", "pip", "Maven", "Gradle", "Composer", "Makefile",
    "Docker Compose", "CI Pipeline", "API Documentation", "Swagger", "OpenAPI", "RESTful Services",
    "Graph Databases", "Neo4j", "Blockchain", "Smart Contracts", "Solidity", "Web3",
    "Metaverse", "Augmented Reality", "Virtual Reality", "Computer Graphics", "Game Development",
    "Unity", "Unreal Engine", "IoT", "Embedded Systems", "Robotics", "Edge Computing",
    "Cloud Infrastructure", "Server Management", "Continuous Monitoring", "Incident Response",
    "Error Handling", "Log Management", "System Monitoring", "Alerting", "Distributed Systems",
    "Concurrency", "Multithreading", "Asynchronous Programming", "Event-Driven Architecture",
    "Clean Code", "Code Maintainability", "Code Quality", "Test Driven Development",
    "Behavior Driven Development", "API Testing", "UI Testing", "Integration",
    "Deployment Automation", "Infrastructure as Code", "Versioning", "Scalable Systems",
    "Fault Tolerance", "High Availability", "Latency Optimization", "Throughput",
    "Data Pipelines", "Message Queues", "Kafka", "RabbitMQ", "Pub/Sub", "Load Balancer",
    "Proxy", "Reverse Proxy", "DNS Management", "Content Delivery Network", "CDN",
    "Data Encryption", "Access Control", "Monitoring Tools", "Performance Metrics",
    "Software Metrics", "Git Workflow", "Branching", "Merging", "Pull Requests", "Code Merge",
    "Peer Review", "Feature Deployment", "Agile Methodology", "Sprint Planning", "Scrum Master",
    "Product Owner", "Software Maintenance", "Debug Logs", "Production Logs", "CI Automation",
    "Continuous Delivery", "Software Deployment", "Container Orchestration", "DevSecOps"
]])

# ---------------- Resume Text Extraction ----------------
def extract_text(file_path):
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

# ---------------- TF-IDF + Weighted Skill Match ----------------
def calculate_match(resume_text, job_desc):
    # Filter JD for keywords only
    jd_filtered_words = [kw for kw in KEYWORDS if kw in job_desc.lower()]
    if not jd_filtered_words:
        return 0, 0, []

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(vocabulary=jd_filtered_words)
    tfidf_matrix = vectorizer.fit_transform([resume_text.lower(), job_desc.lower()])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Extract matched keywords
    matched_keywords = [kw for kw in jd_filtered_words if kw in resume_text.lower()]
    score = len(matched_keywords)
    percentage = (score / len(jd_filtered_words)) * 100

    # Combine TF-IDF similarity with score for ranking
    final_score = similarity * 100 + percentage  # Simple weighted combination

    return final_score, round(percentage, 2), matched_keywords[:10]

# ---------------- Flask Routes ----------------
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
                    "score": round(score, 2),
                    "percentage": percentage,
                    "keywords": common_keywords
                })

            # Sort resumes by descending final score
            ranked_resumes = sorted(ranked_resumes, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", ranked_resumes=ranked_resumes)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
