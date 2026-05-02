# ⚡ WAPDA MDC AI Assistant 🤖
> **"Smart. Secure. AI-Powered."**

[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/ayeshajavid11/wapda-meter-assistant)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Educational-green)](https://github.com/ayeshajavid91-star/wapda-chatbot)

Welcome to the **WAPDA MDC AI Assistant**, a professional-grade, bilingual AI console designed to assist field staff and consumers with Meter Data Control (MDC) and WAPDA operations. This project was developed by **Ayesha Javid** to modernize utility management through artificial intelligence.

---

## 🚀 Live Demo
Experience the full AI console live on Hugging Face:
**[👉 WAPDA MDC Assistant Live Console](https://huggingface.co/spaces/ayeshajavid11/wapda-meter-assistant)**

---

## ✨ Key Features

### 🧠 Intelligent Core
- **Enterprise Knowledge Base**: Over 160+ specialized Q&A pairs covering WAPDA, MEPCO, LESCO, and more.
* **Smart Filter**: Automatically identifies and alerts when "irrelevant questions" are asked.
* **Auto-Suggest**: Real-time, character-by-character search filtering (A-Z) for expert queries.

### 🌍 Multi-Lingual Support
- **English**: Full technical and conversational support.
- **Urdu (Script)**: Understands and responds in Urdu (میٹر، بجلی، بل).
- **Roman Urdu**: Handles conversational phrases like *"MDC ka matlab kia hai?"* or *"Kia hal hai?"*.

### 🎨 Cinematic "Wao" UI
- **ChatGPT/Claude Style**: Large, readable enterprise layout with avatars.
* **Neon Dark Mode**: High-contrast, glowing UI for low-light field use.
* **Interactive Dashboard**: Persistent chat history sidebar and quick-action chips.
* **Smooth Transitions**: Glitch-effect titles and laser-scanning initialization animations.

### 💾 Persistence
- **Session Memory**: Remembers the last 20 messages per session for seamless multi-tasking.
* **Recents List**: Quick access to previous queries in the sidebar.

---

## 🛠️ Tech Stack
- **Backend**: Python 3.9 & Flask
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), and JavaScript (ES6+)
- **Session Management**: Flask-Session
- **Deployment**: Hugging Face Spaces (Dockerized)

---

## 📂 Project Structure
```bash
wapda-chatbot/
├── app.py                 # Core AI Logic & API Endpoints
├── templates/
│   └── index.html        # Enterprise Chat Console UI
├── qa_database.json       # 160+ Question Knowledge Base
├── requirements.txt       # System Dependencies
├── Dockerfile             # Hugging Face Deployment Config
└── README.md              # Project Documentation
```

---

## 🛠️ Local Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/ayeshajavid91-star/wapda-chatbot.git
   cd wapda-chatbot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Console**
   ```bash
   python app.py
   ```
   Access at: `http://localhost:5000`

---

## 👩‍💻 Developed By
**Ayesha Javid**  
*System Engineer & AI Developer*  
*Specializing in Utility Management AI Solutions*

---

## 📜 License
This project is developed for educational and professional demonstration purposes. All rights reserved.

---

*“Empowering WAPDA with Intelligence.”* ⚡
