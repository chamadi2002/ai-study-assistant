import streamlit as st 
import PyPDF2
import google.generativeai as genai

# ✅ 1. Setup Gemini API key
genai.configure(api_key="AIzaSyCSVTLWUxsgQmbd61fxAbrzaERE2mTm0vI")

# ✅ 2. Load Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ✅ 3. Streamlit page setup and styling
st.set_page_config(page_title="📘 AI Study Assistant", layout="wide")

st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        color: #222;
        background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
    }
    label[data-baseweb="file-uploader"] {
        color: #000 !important;        /* black label text */
        font-weight: 700 !important;
        font-size: 1.1em !important;
        margin-bottom: 0.5em !important;
        display: block;
    }
    .stFileUploader label span {
        color: #000 !important;        
        font-weight: 600 !important;
    }
    .stButton>button {
        background-color: #4f8cff;
        color: #fff;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        border: none;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0.3em 0.5em 0.3em 0;
        transition: background 0.2s, opacity 0.2s;
        opacity: 1 !important;
    }
    .stButton>button:disabled {
        background-color: #b3cdfa !important;
        color: #fff !important;
        opacity: 0.7 !important;
        cursor: not-allowed !important;
    }
    .stButton>button:hover:enabled {
        background-color: #2563eb;
        color: #fff;
    }
    .stTextInput>div>div>input {
        background: #f1f5f9;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        padding: 0.5em;
        font-size: 1em;
        color: #222 !important;
    }
    /* ✅ Fix label and placeholder visibility for text input */
.stTextInput label {
    color: #222 !important;  /* label: "Your Question" */
    font-weight: 600;
}

.stTextInput input::placeholder,
.stTextInput input:disabled::placeholder {
    color: #666 !important;
    opacity: 1 !important;
}


    .stSubheader, .stMarkdown h2, .stMarkdown h3 {
        color: #2563eb;
        font-weight: 700;
    }
    .stSpinner {
        color: #4f8cff !important;
    }
    .stAlert {
        border-radius: 8px;
    }
    .stMarkdown {
        background: #fff;
        border-radius: 10px;
        padding: 1.2em 1em;
        margin-bottom: 1em;
        box-shadow: 0 2px 12px rgba(80,120,200,0.07);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📘 AI Study Assistant")

# ✅ File uploader
st.markdown(
    '<span style="color:#444;font-weight:700;font-size:1.1em;">📤 Upload Lecture Slides or PDF</span>',
    unsafe_allow_html=True
)
uploaded_file = st.file_uploader("", type=["pdf"])

# Disable buttons if no file
disabled = uploaded_file is None

# Summary button
if st.button("📝 Generate Summary", disabled=disabled):
    with st.spinner("Generating summary..."):
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        

            prompt = f"Summarize the following content:\n\n{text}"
            response = model.generate_content(prompt)
            st.subheader("📌 Summary:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Summary Error: {e}")

# Flashcards
if st.button("📋 Generate Flashcards", disabled=disabled):
    with st.spinner("Creating flashcards..."):
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            prompt = f"Create 5 flashcards in the format: Question - Answer, from this content:\n\n{text}"
            response = model.generate_content(prompt)
            st.subheader("🧠 Flashcards:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Flashcard Error: {e}")

# Quiz
if st.button("❓ Generate Quiz Questions", disabled=disabled):
    with st.spinner("Creating quiz questions..."):
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            prompt = (
                "Create 5 multiple-choice questions (MCQs) with 4 options and show the correct answer. "
                "Based on this content:\n\n" + text
            )
            response = model.generate_content(prompt)
            st.subheader("📝 Quiz Questions:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Quiz Error: {e}")

# Ask a Question
st.subheader("💬 Ask a Question About the Content")
user_question = st.text_input(
    "Your Question",
    placeholder="Type your question here (e.g., What is the main topic of the lecture?)",
    disabled=disabled
)

if user_question and uploaded_file:
    with st.spinner("Thinking..."):
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            prompt = f"Answer this question based on the content:\n\n{text}\n\nQuestion: {user_question}"
            response = model.generate_content(prompt)
            st.markdown("### 🧠 Answer:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Q&A Error: {e}")
