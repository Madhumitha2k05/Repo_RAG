import git
import shutil
import os
import stat
import time

REPO_DIR = "repositories"


# 🔥 force delete for windows
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repo(repo_url):

    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)

    repo_name = repo_url.split("/")[-1].replace(".git", "")

    repo_path = os.path.join(REPO_DIR, repo_name)

    # =====================================
    # DELETE OLD REPO SAFELY
    # =====================================
    if os.path.exists(repo_path):

        try:
            shutil.rmtree(
                repo_path,
                onerror=remove_readonly
            )

            time.sleep(1)

        except Exception as e:
            print("DELETE ERROR:", e)

    # =====================================
    # CLONE REPO
    # =====================================
    git.Repo.clone_from(
        repo_url,
        repo_path
    )

    return repo_path