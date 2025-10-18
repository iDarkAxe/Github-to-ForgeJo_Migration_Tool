import requests
import subprocess
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Lire les variables depuis .env
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FORGEJO_TOKEN = os.getenv("FORGEJO_TOKEN")
FORGEJO_URL = os.getenv("FORGEJO_URL")

# 1. Liste complète avec visibilité depuis GitHub via gh CLI
result = subprocess.run(
    [
        "gh", "repo", "list", GITHUB_USER,
        "--limit", "1000",
        "--json", "name,url,visibility"
    ],
    capture_output=True,
    text=True
)
repos = json.loads(result.stdout)

# 2. Migration tout en conservant la visibilité d'origine
for repo in repos:
    is_private = repo.get("visibility") == "private"

    payload = {
        "clone_addr": repo["url"],
        "auth_username": GITHUB_USER,
        "auth_password": GITHUB_TOKEN,
        "repo_name": repo["name"],
        "mirror": False,
        "private": is_private,   # Conservation de la visibilité
        "issues": True,
        "pull_requests": True,
        "wiki": True,
        "releases": True,
    }

    r = requests.post(
        f"{FORGEJO_URL}/api/v1/repos/migrate",
        headers={"Authorization": f"token {FORGEJO_TOKEN}"},
        json=payload
        # verify=False  # utile pour SSL auto-signé sur YunoHost
    )

    print(repo["name"], "(privé)" if is_private else "(public)", "→", r.status_code, r.text)

