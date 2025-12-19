# College Website Chatbot using Flask

A lightweight, KB-free, rule-based chatbot integrated into a college website using the Flask web framework.  
The chatbot assists students and visitors by instantly answering common queries related to admissions, courses, fees, placements, hostels, scholarships, and contact details.

---

## 📌 Project Overview

In today’s digital era, educational institutions require efficient systems to handle repetitive student inquiries. This project implements a **rule-based chatbot** that serves as a virtual assistant for a college website. The chatbot eliminates the need for manual query handling by providing instant, accurate, and predefined responses without relying on machine learning models or external knowledge bases.

The application is simple, fast, and easy to deploy, making it ideal for small to medium educational institutions.

---

## 🚀 Features

- KB-free rule-based chatbot
- Integrated college website home page
- Dedicated chatbot interface
- RESTful API for chatbot communication
- Static Q&A matching with keyword fallback
- Session-based local logging of conversations
- Admin endpoints to view logs and static questions
- Beginner-friendly and lightweight architecture

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
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
2️⃣ Create Virtual Environment (Optional but Recommended)
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
/admin/static_qa	View static Q&A data

🔁 Chatbot Working Flow
User enters a query in the chatbot UI

Query is sent to the /chat API

Input is normalized and matched with static Q&A

Keyword-based rules handle partial matches

If no match is found, a fallback response is returned

All interactions are logged locally in JSON format

🔐 Admin Features
View recent chat logs

Monitor unanswered or fallback queries

Review static question-answer pairs

Improve responses based on user interaction history

📌 Use Cases
College websites

Admission help desks

Academic institutions

Student information portals

Internship / academic project demonstrations
