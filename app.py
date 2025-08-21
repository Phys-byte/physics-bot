# app.py
import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

# Initialize OpenAI client using hidden API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Physics Bot", layout="wide")
st.title("📘 Physics Bot for Students")

# Upload PDF
pdf_file = st.file_uploader("Upload your Physics book (PDF)", type="pdf")
if pdf_file:
    reader = PdfReader(pdf_file)
    pages_text = [page.extract_text() for page in reader.pages]
    num_pages = len(pages_text)
    st.success(f"PDF loaded! {num_pages} pages detected.")

# Sidebar: Choose mode
mode = st.sidebar.selectbox(
    "Choose Bot Mode", 
    ["Ask Question", "Summarize Chapter", "Generate Quiz"]
)

# Helper function to create prompts
def make_prompt(mode, user_input, pdf_text=None):
    if mode == "Ask Question":
        return f"""
You are a Physics teaching assistant. Answer the student's question using the following book content:
{''.join(pdf_text)}

- Provide clear explanations
- Solve equations if needed
- Refer to page numbers if relevant
- Use simple examples, graphs, or calculations to explain

Question: {user_input}
"""
    elif mode == "Summarize Chapter":
        return f"""
Summarize the following chapter content in clear bullet points:
{user_input}
"""
    elif mode == "Generate Quiz":
        return f"""
Create a 5-question quiz with answers based on the following content:
{user_input}
"""
    else:
        return user_input

# Mode: Ask Question
if mode == "Ask Question":
    user_question = st.text_input("Ask a question about your Physics book:")
    if st.button("Get Answer") and user_question:
        if not pdf_file:
            st.warning("Please upload a PDF first.")
        else:
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
        prompt = make_prompt(mode, chapter_text)
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
        prompt = make_prompt(mode, chapter_text)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        quiz = response.choices[0].message.content
        st.markdown("### Quiz:")
        st.write(quiz)

# Example graph for visual explanation
st.subheader("Example Graph: y = x^2")
x = list(range(0, 11))
y = [i**2 for i in x]
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("y = x^2")
st.pyplot(fig)
