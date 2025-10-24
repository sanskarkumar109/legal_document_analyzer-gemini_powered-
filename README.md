# Legal Document Analyzer (Gemini-powered)

A simple Streamlit app to **upload legal documents** (PDF or DOCX) and analyze them using **Google Gemini API**.  
The app can:

- Summarize the document
- Extract key clauses
- Detect missing clauses
- Act as a chatbot to answer questions based on the document

Everything runs in a **single file** (`app.py`) — no backend required.

---

## Features

1. **Upload PDF/DOCX:** Quickly upload your legal document.
2. **Summarize Document:** Get an executive summary and section-wise summaries.
3. **Extract Clauses:** Automatically detect key clauses in the document.
4. **Find Missing Clauses:** Compare with standard templates and highlight missing clauses.
5. **Chat with Document:** Ask questions and get answers based on the uploaded document.

---

## Requirements

- Python 3.9+
- Streamlit
- google-generativeai (Gemini SDK)
- pdfplumber
- python-docx
- Optional: python-dotenv (if using `.env` for API key)

Install dependencies:

```bash
pip install streamlit google-generativeai pdfplumber python-docx
