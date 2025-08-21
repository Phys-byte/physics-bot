import os
import streamlit as st
import openai
import PyPDF2
import matplotlib.pyplot as plt

# Load API key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Helper: Extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_by_page = {}
    for i, page in enumerate(pdf_reader.pages):
        text_by_page[i+1] = page.extract_text()
    return text_by_page

# --- Load PDF ---
@st.cache_resource
def load_pdf():
    with open("Physics_1.pdf", "rb") as f:
        return extract_text_from_pdf(f)

pdf_text = load_pdf()

# --- Streamlit UI ---
st.title("📘 Physics_1 Student Bot")
st.write("Ask me questions about the Physics_1 textbook. I can summarize, find pages, solve problems, and make quizzes.")

mode = st.sidebar.selectbox(
    "Choose mode",
    ["Ask Question", "Summary", "Find Pages", "Solve Equation", "Make Quiz"]
)

# --- 1. Ask Question ---
if mode == "Ask Question":
    query = st.text_input("Enter your question:")
    if st.button("Ask"):
        context = " ".join(list(pdf_text.values())[:5])  # simple context (first 5 pages)
        prompt = f"You are a Physics tutor. Use the book content:\n\n{context}\n\nQuestion: {query}\nAnswer clearly for a student."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        st.write(response["choices"][0]["message"]["content"])

# --- 2. Summary ---
elif mode == "Summary":
    pages = st.text_input("Enter pages (e.g., 10-15):")
    if st.button("Summarize"):
        start, end = map(int, pages.split("-"))
        context = " ".join([pdf_text[i] for i in range(start, end+1) if i in pdf_text])
        prompt = f"Summarize this content in simple student-friendly language:\n{context}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        st.write(response["choices"][0]["message"]["content"])

# --- 3. Find Pages ---
elif mode == "Find Pages":
    keyword = st.text_input("Enter keyword (e.g., Newton's Laws):")
    if st.button("Search"):
        results = []
        for page, text in pdf_text.items():
            if keyword.lower() in text.lower():
                results.append(page)
        if results:
            st.write(f"📖 Found on pages: {results}")
        else:
            st.write("❌ Not found.")

# --- 4. Solve Equation ---
elif mode == "Solve Equation":
    equation = st.text_input("Enter equation (e.g., 2*5+3):")
    if st.button("Solve"):
        try:
            result = eval(equation)
            st.success(f"Result: {result}")
            # Example plot
            x = range(-10, 11)
            y = [eval(equation.replace("x", str(val))) for val in x]
            fig, ax = plt.subplots()
            ax.plot(x, y)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {e}")

# --- 5. Make Quiz ---
elif mode == "Make Quiz":
    topic = st.text_input("Enter topic for quiz (e.g., Kinematics):")
    if st.button("Generate Quiz"):
        context = " ".join(list(pdf_text.values())[:10])
        prompt = f"Create 5 quiz questions (multiple-choice) about {topic} based on this book content:\n{context}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        st.write(response["choices"][0]["message"]["content"])
