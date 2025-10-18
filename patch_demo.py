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
FORGEJO_USER = os.getenv("FORGEJO_USER")
FORGEJO_TOKEN = os.getenv("FORGEJO_TOKEN")
FORGEJO_URL = os.getenv("FORGEJO_URL")

# 1. Lister les repos GitHub avec visibilité
result = subprocess.run(
    ["gh", "repo", "list", GITHUB_USER, "--limit", "1000", "--json", "name,isPrivate"],
    capture_output=True,
    text=True
)
repos = json.loads(result.stdout)

headers = {"Authorization": f"token {FORGEJO_TOKEN}"}

for repo in repos:
    name = repo["name"]
    should_be_private = (repo["isPrivate"] == True)

    # 2. Récupérer l'état actuel sur Forgejo
    r = requests.get(
        f"{FORGEJO_URL}/api/v1/repos/{FORGEJO_USER}/{name}",
        headers=headers,
        verify=False   # mettre un chemin vers ton cert si besoin
    )

    if r.status_code != 200:
        print(f"⚠️ Impossible de lire {name} sur Forgejo (status {r.status_code})")
        continue

    forgejo_repo = r.json()
    is_private_now = forgejo_repo["private"]

    # 3. Corriger si nécessaire
    if should_be_private != is_private_now:
        patch = {"private": should_be_private}
        r2 = requests.patch(
            f"{FORGEJO_URL}/api/v1/repos/{FORGEJO_USER}/{name}",
            headers=headers,
            json=patch,
            verify=False
        )
        if r2.status_code == 200:
            state = "privé" if should_be_private else "public"
            print(f"✅ Corrigé {name} → {state}")
        else:
            print(f"❌ Erreur pour {name}: {r2.status_code} {r2.text}")
    else:
        print(f"✔️ {name} déjà correct")

