# 📚 StudySnap - AI Study Assistant

StudySnap is an AI-powered study assistant built using Python, Streamlit, and Google Gemini.

## 🚀 What does StudySnap do?

StudySnap helps students understand questions, diagrams, and study notes using AI.

The user can:

- 📸 Upload a photo of a question or study material
- 🤖 Get a simple explanation using Gemini Vision
- 💬 Ask follow-up questions
- 📧 Send the explanation to an email address

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Gemini Vision
- Gmail SMTP

## 🔄 How it works

Photo / Study Material
→ Gemini Vision
→ AI Explanation
→ Follow-up Chat
→ Email Summary

## ▶️ Run Locally

### 1. Clone the repository
git clone YOURGITHUBREPOSITORY_URL


### 2. Create a virtual environment
python -m venv venv


### 3. Activate the virtual environment
Windows PowerShell:
.\venv\Scripts\Activate.ps1


### 4. Install dependencies
pip install -r requirements.txt


### 5. Add API keys
Create:

.streamlit/secrets.toml
Add your Gemini API key and Gmail App Password.

### 6. Run the application
streamlit run app.py


## 🔐 Security
API keys and passwords are stored in `.streamlit/secrets.toml` and are not committed to GitHub.

## 👨‍💻 Project
Built as an AI Vision project using Gemini Vision and Streamlit.