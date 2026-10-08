import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types


# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="StudySnap",
    page_icon="📚"
)


# -----------------------------
# API keys and email settings
# -----------------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


# -----------------------------
# Connect to Gemini
# -----------------------------
client = genai.Client(api_key=GEMINI_API_KEY)


# -----------------------------
# Email function
# -----------------------------
def send_email(to_address, subject, body):

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        server.send_message(message)


# -----------------------------
# App title
# -----------------------------
st.title("📚 StudySnap")

st.write(
    "Upload a question or study material "
    "and get a simple AI explanation."
)


# -----------------------------
# Chat history
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []


# -----------------------------
# Upload image
# -----------------------------
uploaded_file = st.file_uploader(
    "📸 Upload a question, diagram, or study notes",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()

    st.image(
        image_bytes,
        caption="Uploaded study material",
        use_container_width=True
    )


    # -----------------------------
    # Explain image
    # -----------------------------
    if st.button("🤖 Explain this"):

        with st.spinner("Reading your study material..."):

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=[

                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    ),

                    """
                    You are StudySnap, an AI study assistant.

                    Carefully analyze the uploaded image.

                    If it contains a question, problem, diagram,
                    textbook content, or study notes:

                    1. Identify what is shown.
                    2. Explain it in simple language.
                    3. Give an example when useful.
                    4. If it is a question, explain the answer step by step.

                    Stay focused on the uploaded study material.
                    Do not introduce unrelated topics.

                    Keep the explanation clear and student-friendly.
                    """
                ]
            )

            explanation = response.text

            st.session_state.chat.append(
                {
                    "role": "assistant",
                    "content": explanation
                }
            )


# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.chat:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# -----------------------------
# Follow-up questions
# -----------------------------
if uploaded_file is not None and st.session_state.chat:

    question = st.chat_input(
        "💬 Ask a follow-up question..."
    )

    if question:

        st.chat_message("user").write(question)

        with st.spinner("Thinking..."):

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=[
                    """
                    You are StudySnap, a friendly AI study assistant.

                    Answer the student's question clearly,
                    simply, and directly.

                    Stay focused on the study topic.
                    """,

                    question
                ]
            )

            answer = response.text

            st.session_state.chat.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            st.session_state.chat.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


# -----------------------------
# Send explanation by email
# -----------------------------
if st.session_state.chat:

    st.divider()

    st.subheader("📧 Save your explanation")

    email_address = st.text_input(
        "Enter email address"
    )

    if st.button("📧 Send Explanation to Email"):

        if not email_address.strip():

            st.warning(
                "Please enter an email address."
            )

        else:

            # Combine the conversation
            email_body = "\n\n".join(
                message["content"]
                for message in st.session_state.chat
            )

            try:

                send_email(
                    email_address,
                    "StudySnap - Your Study Explanation",
                    email_body
                )

                st.success(
                    "✅ Explanation sent successfully! "
                    "Check your email."
                )

            except Exception as error:

                st.error(
                    f"❌ Email could not be sent: {error}"
                )