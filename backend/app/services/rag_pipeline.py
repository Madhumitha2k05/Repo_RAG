from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

from groq import Groq
import os

# ============================================
# LOAD ENV VARIABLES
# ============================================
load_dotenv()

# ============================================
# GROQ CLIENT
# ============================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ============================================
# GLOBAL VECTOR DATABASE
# ============================================
vector_db = None

# ============================================
# LOAD REPOSITORY
# ============================================
def load_repo(repo_path):

    global vector_db

    documents = []

    print("📂 Loading repository...")

    # ============================================
    # READ FILES
    # ============================================
    for root, dirs, files in os.walk(repo_path):

        for file in files:

            # Supported file types
            if file.endswith((
                ".py",
                ".js",
                ".ts",
                ".html",
                ".css",
                ".md",
                ".txt",
                ".json",
                ".yaml",
                ".yml"
            )):

                try:

                    file_path = os.path.join(root, file)

                    with open(file_path, "r", encoding="utf-8") as f:

                        content = f.read()

                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "source": file
                                }
                            )
                        )

                except Exception as e:
                    print("❌ Error reading file:", e)

    # ============================================
    # SPLIT DOCUMENTS
    # ============================================
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    print(f"✅ Total chunks created: {len(docs)}")

    # ============================================
    # LOAD EMBEDDING MODEL
    # (INSIDE FUNCTION FOR RENDER MEMORY FIX)
    # ============================================
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ============================================
    # CREATE VECTOR DATABASE
    # ============================================
    vector_db = FAISS.from_documents(
        docs,
        embeddings
    )

    print("✅ VECTOR DATABASE CREATED")

    return "✅ Repository Loaded Successfully!"

# ============================================
# ASK QUESTION
# ============================================
def ask_question(query):

    global vector_db

    try:

        # ============================================
        # RAG MODE
        # ============================================
        if vector_db is not None:

            docs = vector_db.similarity_search(
                query,
                k=5
            )

            # No relevant docs found
            if not docs:

                return "I could not find this in the uploaded repository."

            # ============================================
            # BUILD CONTEXT
            # ============================================
            context = ""

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown File"
                )

                context += f"""

FILE: {source}

CODE:
{doc.page_content}

====================================================
"""

            # ============================================
            # FINAL PROMPT
            # ============================================
            final_prompt = f"""
You are RepoCode AI.

You MUST answer ONLY using the repository content below.

STRICT RULES:
1. DO NOT give general programming explanations
2. DO NOT use outside knowledge
3. ONLY answer from repository code
4. Mention filenames when possible
5. If answer is not found, say:
"I could not find this in the uploaded repository."

====================================================
REPOSITORY CONTENT
====================================================

{context}

====================================================
QUESTION
====================================================

{query}

====================================================
ANSWER
====================================================
"""

        # ============================================
        # NORMAL CHATBOT MODE
        # ============================================
        else:

            final_prompt = query

        # ============================================
        # SEND TO GROQ
        # ============================================
        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"