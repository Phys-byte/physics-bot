# app.py
import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import re

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Physics Bot", layout="wide")
st.title("Physics Bot for Students")

# Upload PDF
pdf_file = st.file_uploader("Upload your Physics book (PDF)", type="pdf")
if pdf_file:
    reader = PdfReader(pdf_file)
    pages_text = [page.extract_text() for page in reader.pages]
    st.success("PDF loaded successfully!")
    num_pages = len(pages_text)

# Sidebar: choose mode
mode = st.sidebar.selectbox("Choose Bot Mode", ["Ask Question", "Summarize Chapter", "Generate Quiz"])

# Helper function to create prompt
def make_prompt(mode, user_input, pages_text):
    if mode == "Ask Question":
        return f"""
You are a Physics teaching assistant. The student has access to the following book content:
{''.join(pages_text)}

Answer the question accurately. Include calculations, examples, graphs (described in text), and refer to page numbers if possible.

Question: {user_input}
"""
    elif mode == "Summarize Chapter":
        return f"""
You are a Physics assistant. Summarize the following text clearly in bullet points:
{user_input}
"""
    elif mode == "Generate Quiz":
        return f"""
You are a Physics teacher. Based on the following content, generate a short quiz of 5 questions with answers:
{user_input}
"""

# Mode: Ask Question
if mode == "Ask Question":
    user_question = st.text_input("Ask a question about your Physics book:")
    if st.button("Get Answer") and user_question:
        if not pdf_file:
            st.warning("Please upload a PDF first.")
        else:
            # Send to OpenAI
            prompt = make_prompt(mode, user_question, pages_text)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.choices[0].message.content
            st.markdown("### Answer:")
            st.write(answer)

# Mode: Summarize Chapter
elif mode == "Summarize Chapter":
    chapter_number = st.number_input("Enter chapter number to summarize", min_value=1, max_value=num_pages)
    if st.button("Summarize"):
        chapter_text = pages_text[chapter_number-1]
        prompt = make_prompt(mode, chapter_text, None)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        summary = response.choices[0].message.content
        st.markdown("### Chapter Summary:")
        st.write(summary)

# Mode: Generate Quiz
elif mode == "Generate Quiz":
    chapter_number = st.number_input("Enter chapter number for quiz", min_value=1, max_value=num_pages)
    if st.button("Generate Quiz"):
        chapter_text = pages_text[chapter_number-1]
        prompt = make_prompt(mode, chapter_text, None)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        quiz = response.choices[0].message.content
        st.markdown("### Quiz:")
        st.write(quiz)

# Example: graph generation
st.subheader("Graph Example")
x = list(range(0, 11))
y = [i**2 for i in x]
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Example: y = x^2")
st.pyplot(fig)
