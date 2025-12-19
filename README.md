# AI-Powered College Website Chatbot using Flask and NLP

An AI-powered chatbot integrated into a college website using the Flask web framework.  
The chatbot leverages Natural Language Processing (NLP) techniques such as **TF-IDF vectorization** and **cosine similarity** to intelligently respond to student and visitor queries related to admissions, courses, fees, placements, hostels, scholarships, and contact details.

---

## 📌 Project Overview

Educational institutions often receive repetitive queries from students and parents regarding admissions and campus facilities. This project addresses that challenge by implementing an **AI-powered chatbot** that provides instant and accurate responses.

Initially designed as a rule-based system, the chatbot was enhanced using **NLP-based semantic similarity**, allowing it to understand user intent even when queries are phrased differently. The system does not rely on external APIs or large language models, making it lightweight, cost-effective, and suitable for academic deployment.

---

## 🚀 Features

- AI-powered chatbot using NLP techniques
- Semantic query matching using TF-IDF and cosine similarity
- Integrated college website home page
- Dedicated chatbot interface
- RESTful API for chatbot communication
- Fallback handling for unmatched queries
- Session-based local logging of user interactions
- Admin endpoints to view logs and static Q&A
- Lightweight, fast, and easy to deploy

---

## 🧠 AI & NLP Approach

The chatbot uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to convert both user queries and predefined questions into numerical feature vectors. **Cosine similarity** is then applied to measure semantic similarity between the vectors.

The response corresponding to the highest similarity score above a defined threshold is selected and returned to the user. This approach enables intelligent query handling without requiring exact keyword matches, making the chatbot flexible and AI-driven.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **AI / NLP:** TF-IDF, Cosine Similarity, Scikit-learn, NumPy  
- **Frontend:** HTML, CSS, JavaScript  
- **Data Storage:** JSON (static Q&A and logs)  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure

college-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│ ├── index.html
│ └── chatbot.html
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
│
└── logs.json (ignored in Git)

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sidra2710/college-chatbot.git
cd college-chatbot
2️⃣ Create Virtual Environment (Optional)
bash
Copy code
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Application
bash
Copy code
python app.py
🌐 Application Routes
Route	Description
/	College website home page
/chatbot	Chatbot user interface
/chat	Chat API endpoint
/admin/logs	View chatbot interaction logs
/admin/static_qa	View static Q&A dataset

🔁 System Workflow
User enters a query via the chatbot UI

Query is sent to the /chat API

Input is vectorized using TF-IDF

Cosine similarity is calculated against stored questions

Best-matching response is selected

If similarity is low, fallback logic is applied

Interaction is logged locally for analysis

📌 Use Cases
College and university websites

Admission enquiry systems

Student help desks

Academic and internship projects

AI/NLP learning demonstrations
