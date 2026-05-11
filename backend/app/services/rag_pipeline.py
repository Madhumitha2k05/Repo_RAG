from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
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

vector_db = {}

# ============================================
# LOAD REPOSITORY
# ============================================

def load_repo(repo_path):

    global vector_db

    documents = []

    print("\n📂 Loading repository...")

    # ============================================
    # READ FILES
    # ============================================

    for root, dirs, files in os.walk(repo_path):

        for file in files:

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

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()

                        if content.strip():

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

    print(f"\n✅ Total files loaded: {len(documents)}")

    # ============================================
    # SPLITTER
    # ============================================

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    print(f"\n✅ Total chunks created: {len(docs)}")

    # ============================================
    # EMBEDDINGS
    # ============================================

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ============================================
    # VECTOR DB
    # ============================================

    vector_db["db"] = FAISS.from_documents(
        docs,
        embeddings
    )

    print("\n✅ VECTOR DATABASE CREATED")

    return "✅ Repository Loaded Successfully!"


# ============================================
# ASK QUESTION
# ============================================

def ask_question(query, use_repo=False):

    global vector_db

    try:

        # ============================================
        # GENERAL CHATBOT MODE
        # ============================================

        if use_repo == False:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],

                temperature=0.3
            )

            return response.choices[0].message.content

        # ============================================
        # REPOSITORY MODE
        # ============================================

        if "db" not in vector_db:

            return "Please load a repository first."

        docs = vector_db["db"].similarity_search(
            query + " repository source code function class file",
            k=15
        )

        print(f"\n🔥 Retrieved Docs: {len(docs)}")

        if len(docs) == 0:

            return "I could not find this in the uploaded repository."

        # ============================================
        # CONTEXT
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
        # PROMPT
        # ============================================

        final_prompt = f"""
You are RepoCode AI.

You MUST answer ONLY from the uploaded repository.

STRICT RULES:
1. NEVER give generic programming explanations
2. NEVER use outside knowledge
3. ALWAYS answer from repository code
4. Mention filenames whenever possible
5. Explain functions/classes/files ONLY from repository
6. If answer not found, say:
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
ANSWER FROM REPOSITORY ONLY
====================================================
"""

        # ============================================
        # GROQ RESPONSE
        # ============================================

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"