from fastapi import APIRouter
from pydantic import BaseModel

from app.services.github_loader import clone_repo
from app.services.rag_pipeline import load_repo

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: str


@router.post("/load_repo")
def load_repository(data: RepoRequest):

    try:

        print("\n🔥 RECEIVED REPO URL:")
        print(data.repo_url)

        # STEP 1: CLONE REPO
        repo_path = clone_repo(data.repo_url)

        print("\n✅ REPO CLONED TO:")
        print(repo_path)

        # STEP 2: CREATE VECTOR DB
        result = load_repo(repo_path)

        print("\n✅ VECTOR DB CREATED")

        return {
            "message": result
        }

    except Exception as e:

        print("\n❌ ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }