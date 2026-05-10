# 🤖 Repo_RAG

An AI-powered Repository Assistant built using **RAG (Retrieval Augmented Generation)** architecture.

Repo RAG allows users to upload GitHub repositories and ask intelligent questions about the codebase in natural language.  
The system retrieves relevant code snippets using embeddings and vector search, then generates accurate repository-based responses using LLMs.

---

## 🚀 Features

- 📂 Upload Public GitHub Repositories
- 💬 Ask Questions About Codebases
- 🧠 RAG-Based Repository Understanding
- 🔍 FAISS Vector Database Search
- ⚡ Fast Repository Retrieval
- 🤖 AI-Powered Code Explanations
- 🎨 Beautiful Streamlit User Interface
- 🔗 Groq LLM Integration
- 📄 Multi-file Repository Analysis
- 🧩 Supports Python, JS, HTML, CSS, JSON and more

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core Backend |
| FastAPI | Backend API |
| Streamlit | Frontend UI |
| LangChain | RAG Pipeline |
| FAISS | Vector Database |
| HuggingFace | Embeddings |
| Groq API | LLM Responses |
| GitPython | Repository Cloning |

---

## 🏗️ Architecture

```text
User Question
      ↓
Repository Loader
      ↓
Text Chunking
      ↓
Embeddings Generation
      ↓
FAISS Vector Store
      ↓
Similarity Search
      ↓
Groq LLM
      ↓
AI Response
```

---

## 📂 Project Structure

```text
Repo_RAG/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── repositories/
│   └── venv/
│
├── frontend/
│   └── app.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

---

### 2️⃣ Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

---

### 4️⃣ Run Backend

```bash
python -m uvicorn app.main:app --reload
```

---

### 5️⃣ Run Frontend

Open another terminal:

```bash
cd frontend

streamlit run app.py
```

---

## 💡 Example Questions

- Explain `app.py` in this repository
- What is the purpose of `rag_pipeline.py`?
- Which file handles API routes?
- Explain the authentication flow
- How does the vector database work?

---

## 🔥 Future Enhancements

- 📄 PDF Documentation Support
- 🧠 Better Code Summarization
- 🌐 Multi-Repository Chat
- 🎙️ Voice Assistant Integration
- 📊 Repository Visualization
- ☁️ Cloud Deployment

---

## 👩‍💻 Developer

**Madhumitha K**  
B.Tech Artificial Intelligence & Data Science Student 🚀

---

