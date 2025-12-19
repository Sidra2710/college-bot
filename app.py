# app.py  -- KB-free minimal chatbot backend + college website home
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import os
import time
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ---------- Config ----------
LOGS_PATH = os.environ.get('CHAT_LOGS_PATH', 'logs.json')
FALLBACK_REPLY = os.environ.get(
    'FALLBACK_REPLY',
    "Sorry, I couldn't find an answer. Would you like me to forward this to an admin?"
)

# ---------- Simple rule-based "knowledge" (optional) ----------
# NOTE: keys are all LOWERCASE (see chat() where we use text.lower()).
STATIC_QA = {
    # ---------- Greetings ----------
    "hi": "Hello, I am Sidra. How can I help you?",
    "hello": "Hello! How can I assist you today?",
    "hey": "Hi there! How can I help?",

    # ---------- Admissions ----------
    "when is admission deadline?": "Admissions close on July 31 every year.",
    "what is the admission deadline": "Admissions close on July 31 every year.",
    "when is the last day for submission?": "The last day for submission of application forms is 31 July.",
    "how to apply for admission": "You can apply online through our official college website.",
    "admission process": "Admissions are based on entrance exams and merit as per university norms.",

    # ---------- Courses ----------
    "what are the courses that you are offering?":
        "We offer B.Tech in CSE, ECE, ME, Civil, and AI&DS, plus MBA and MCA programmes.",
    "courses offered": "We offer B.Tech, MBA, and MCA programs in multiple specializations.",
    "btech courses": "B.Tech is available in CSE, ECE, ME, Civil, and AI & Data Science.",

    # ---------- College Location ----------
    "where is the campus located?": "Our campus is located at Vertex College, Jesus Main Road, ZA, Nor, 10300.",
    "college address": "Our campus is located at Vertex College, Jesus Main Road, ZA, Nor, 10300.",

    # ---------- Contact ----------
    "how to contact admissions": "You can email info@vertexcollege.ac.in or call +91-98765 43210.",
    "contact number": "You can call us at +91-98765 43210.",
    "email id": "You can email us at info@vertexcollege.ac.in.",

    # ---------- Website ----------
    "what is your college website?": "You can visit our college website at http://127.0.0.1:5000/",
    "provide me the college website": "Here is our college website: http://127.0.0.1:5000/",
    "college website link": "Visit our official website at http://127.0.0.1:5000/",

    # ---------- Fee Structure ----------
    "fee structure": "The annual fee ranges from ₹70,000 to ₹1,20,000 depending on the course.",
    "btech fees": "The B.Tech annual fee is approximately ₹1,00,000.",
    "mba fees": "The MBA annual fee is approximately ₹1,20,000.",
    "mca fees": "The MCA annual fee is approximately ₹90,000.",

    # ---------- Hostel ----------
    "hostel facility": "Yes, separate hostel facilities are available for both boys and girls.",
    "hostel fees": "The hostel fee is approximately ₹60,000 per year including food.",
    "is hostel available": "Yes, secure hostel accommodation is available inside the campus.",

    # ---------- Placements ----------
    "placements": "Vertex College has a 90% placement rate with top recruiters every year.",
    "placement details": "Our highest package is ₹12 LPA and average package is ₹4.5 LPA.",
    "companies visiting": "Top recruiters include TCS, Infosys, Wipro, Amazon, and Capgemini.",

    # ---------- Scholarship ----------
    "scholarship": "Scholarships are available for merit students and government category students.",
    "scholarship details": "Students can apply for state and central government scholarships.",
    "fee concession": "Fee concession is provided to eligible students under scholarship schemes.",

    # ---------- Faculty ----------
    "faculty details": "Our faculty members are highly experienced and most hold PhD qualifications.",
    "teaching staff": "We have well-qualified and industry-experienced teaching staff.",
    "professors": "Our professors are experts in their respective domains.",

    # ---------- Library & Labs ----------
    "library": "Our digital library is equipped with over 50,000 books and online journals.",
    "lab facilities": "We have modern computer labs, electronics labs, and research centers.",
    "computer lab": "Our computer labs are equipped with high-speed internet and latest systems."
}

# ---------- AI / NLP Model (TF-IDF + Cosine Similarity) ----------

questions = list(STATIC_QA.keys())
answers = list(STATIC_QA.values())

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def get_ai_reply(user_input):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)[0]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    if best_score > 0.35:   # threshold
        return answers[best_idx], float(best_score)
    else:
        return None, 0.0

# ---------- Local logging helpers ----------
def append_log(entry):
    try:
        if os.path.exists(LOGS_PATH):
            with open(LOGS_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
    except Exception:
        logs = []
    logs.append(entry)
    try:
        with open(LOGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print("Failed to write logs:", e)


# ---------- Routes ----------

# 1) College website home page
@app.route('/')
def home():
    # NEW: this now serves your college website (templates/index.html)
    return render_template('index.html')


# 2) Chatbot UI page (your old index.html, renamed to chatbot.html)
@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')


# 3) Chat API used by the chatbot front-end
@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json() or {}
    text = (payload.get('text') or '').strip()
    session_id = payload.get('session_id') or request.remote_addr or 'anonymous'

    if not text:
        return jsonify({'reply': "Please type a message.", 'source': 'error', 'score': 0.0})

    low = text.lower().strip()
    reply = None
    source = 'static'
    score = 1.0

    # exact match on lowercased keys
    # 1) AI-based semantic matching
    reply, score = get_ai_reply(low)
    source = 'ai'

# 2) If AI fails, fallback to rule-based logic
    if not reply:
        source = 'rule'
        score = 0.6

        if any(w in low for w in ['admission', 'admissions', 'deadline', 'apply']):
            reply = "Admissions deadlines vary by program; please check the admissions page or email admissions@college.edu."

        elif any(w in low for w in ['contact', 'phone', 'call', 'email']):
            reply = "You can contact admin at admin@college.edu or call +1-555-1234."

        elif any(w in low for w in ['website', 'link', 'url']):
            reply = "You can visit our college website at http://127.0.0.1:5000/."

        else:
            reply = FALLBACK_REPLY
            source = 'fallback'
            score = 0.0


    if not reply:
        # 2) simple keyword rules (very small)
        if any(w in low for w in ['admission', 'admissions', 'deadline', 'apply']):
            reply = "Admissions deadlines vary by program; please check the admissions page or email admissions@college.edu."
            source = 'rule'
            score = 0.6

        elif any(w in low for w in ['contact', 'phone', 'call', 'email']):
            reply = "You can contact admin at admin@college.edu or call +1-555-1234."
            source = 'rule'
            score = 0.6

        # 👉 NEW: website / link questions
        elif any(w in low for w in ['website', 'link', 'url']):
            reply = "You can visit our college website at http://127.0.0.1:5000/."
            # when you deploy online, change the URL above to your real website
            source = 'rule'
            score = 0.9

        else:
            # 3) fallback
            reply = FALLBACK_REPLY
            source = 'fallback'
            score = 0.0

    # log chat locally
    log_entry = {
        'session': session_id,
        'query': text,
        'reply': reply,
        'source': source,
        'score': score,
        'ts': time.time()
    }
    append_log(log_entry)

    return jsonify({'reply': reply, 'source': source, 'score': score})


# ---------- (Optional) simple admin endpoints to view logs or static QA ----------

@app.route('/admin/logs', methods=['GET'])
def get_logs():
    try:
        if os.path.exists(LOGS_PATH):
            with open(LOGS_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
    except Exception:
        logs = []
    # return most recent first
    logs = list(reversed(logs))[:500]
    return jsonify(logs)


@app.route('/admin/static_qa', methods=['GET'])
def list_static_qa():
    data = [{'question': k, 'answer': v} for k, v in STATIC_QA.items()]
    return jsonify(data)


if __name__ == '__main__':
    print("Starting KB-free chatbot. Logs:", LOGS_PATH)
    app.run(host='0.0.0.0', port=5000, debug=True)


