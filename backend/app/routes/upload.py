from fastapi import APIRouter
from pydantic import BaseModel

from app.services.github_loader import clone_repo
from app.services.rag_pipeline import load_repo

router = APIRouter()

# ============================================
# REQUEST MODEL
# ============================================

class RepoRequest(BaseModel):
    repo_url: str

# ============================================
# LOAD REPOSITORY
# ============================================

@router.post("/load_repo")
def load_repository(data: RepoRequest):

    try:

        print("\n🔥 RECEIVED REPO URL:")
        print(data.repo_url)

        # ============================================
        # CLONE REPOSITORY
        # ============================================

        repo_path = clone_repo(data.repo_url)

        print("\n✅ REPOSITORY CLONED:")
        print(repo_path)

        # ============================================
        # CREATE VECTOR DATABASE
        # ============================================

        result = load_repo(repo_path)

        return {
            "message": result
        }

    except Exception as e:

        print("\n❌ ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }