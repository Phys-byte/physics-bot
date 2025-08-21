import streamlit as st
from openai import OpenAI
import PyPDF2
import os

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(page_title="Physics Student Bot", layout="wide")
st.title("Physics Student Bot 📚")

# Load OpenAI API key from secrets
api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key)

# -----------------------------
# Upload PDF
# -----------------------------
uploaded_file = st.file_uploader("Upload your Physics PDF", type=["pdf"])
pdf_text = ""

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() + "\n"
    st.success(f"Loaded {len(pdf_reader.pages)} pages from {uploaded_file.name}.")

# -----------------------------
# Bot Interaction
# -----------------------------
st.subheader("Ask your Physics questions")

user_question = st.text_input("Type your question here:")

if user_question and pdf_text:
    prompt = f"""
You are a Physics teacher AI. Use the following text from a book to answer the student's question carefully.
Book content:
{pdf_text}

Student question:
{user_question}
"""

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

    answer = response.choices[0].message.content
    st.markdown("**Answer:**")
    st.write(answer)

# -----------------------------
# Generate Summary
# -----------------------------
if uploaded_file:
    if st.button("Generate Book Summary"):
        prompt_summary = f"""
You are a Physics teacher AI. Summarize the following book content in clear bullet points:
{pdf_text}
"""
        with st.spinner("Generating summary..."):
            response_summary = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_summary}],
                temperature=0.7
            )
        summary = response_summary.choices[0].message.content
        st.markdown("**Summary:**")
        st.write(summary)

# -----------------------------
# Generate Quiz
# -----------------------------
if uploaded_file:
    if st.button("Generate a Quiz"):
        prompt_quiz = f"""
You are a Physics teacher AI. Based on the following text, create a short quiz of 5 questions with answers.
Book content:
{pdf_text}
"""
        with st.spinner("Generating quiz..."):
            response_quiz = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_quiz}],
                temperature=0.7
            )
        quiz = response_quiz.choices[0].message.content
        st.markdown("**Quiz:**")
        st.write(quiz)
