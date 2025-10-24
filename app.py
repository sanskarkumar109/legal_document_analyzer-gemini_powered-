import streamlit as st
import pdfplumber
import docx2txt
import google.generativeai as genai
import tempfile
import os

# ------------------ CONFIG ------------------
genai.configure(api_key=("AIzaSyB7lY1KDg6_8kiCs1vbOndj2ekLjqc-FQw"))
model = genai.GenerativeModel("gemini-2.5-pro") 
st.set_page_config(page_title="Legal Document Analyzer", layout="wide")

# ------------------ FUNCTIONS ------------------
def extract_text(file):
    """Extract text from PDF or DOCX."""
    name = file.name.lower()
    if name.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        text = ""
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif name.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        text = docx2txt.process(tmp_path)
        return text
    else:
        st.error("Only PDF and DOCX files are supported.")
        return ""

def summarize_text(text):
    prompt = f"""
    You are a legal assistant. Summarize the following legal document.
    Provide:
    1. Executive Summary (3-5 lines)
    2. Section-wise Summary (if applicable)
    Document:
    {text[:20000]}  # limiting to avoid token overflow
    """
    response = model.generate_content(prompt)
    return response.text

def extract_clauses(text):
    prompt = f"""
    Extract all key clauses from the following legal document.
    For each clause, return:
    - Clause Title
    - Clause Summary (1-2 lines)
    - Confidence (0 to 1)
    Document:
    {text[:20000]}
    """
    response = model.generate_content(prompt)
    return response.text

def detect_missing_clauses(text):
    prompt = f"""
    You are a legal expert. Compare this document to a standard contract.
    Identify which important clauses are missing or incomplete.
    Document:
    {text[:20000]}
    Output format:
    - Missing Clauses: [list]
    - Explanation for each missing clause
    """
    response = model.generate_content(prompt)
    return response.text

def chat_with_doc(text, user_query):
    prompt = f"""
    You are a helpful legal assistant. Answer based ONLY on this document:
    {text[:20000]}

    Question: {user_query}
    """
    response = model.generate_content(prompt)
    return response.text

# ------------------ STREAMLIT UI ------------------
st.title("⚖️ Legal Document Analyzer (Gemini-powered)")
st.markdown("Upload a **legal document** (PDF or DOCX) to summarize, extract key clauses, find missing clauses, and chat with it.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx"])

if uploaded_file:
    st.success("File uploaded successfully!")
    text = extract_text(uploaded_file)

    if st.button("Summarize Document"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
        st.subheader("📘 Executive & Section Summary")
        st.write(summary)

    if st.button("Extract Clauses"):
        with st.spinner("Extracting clauses..."):
            clauses = extract_clauses(text)
        st.subheader("📑 Extracted Clauses")
        st.write(clauses)

    if st.button("Find Missing Clauses"):
        with st.spinner("Analyzing missing clauses..."):
            missing = detect_missing_clauses(text)
        st.subheader("🚫 Missing Clauses")
        st.write(missing)

    st.markdown("---")
    st.subheader("💬 Chat with Your Document")
    user_query = st.text_input("Ask a question about this document:")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            answer = chat_with_doc(text, user_query)
        st.write(answer)
