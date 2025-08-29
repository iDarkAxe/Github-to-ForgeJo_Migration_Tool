import requests
import subprocess
import json

GITHUB_USER = "username"
GITHUB_TOKEN = "xxxx"
FORGEJO_URL = "https://yourForgeJoURLshouldBeHere/"
FORGEJO_TOKEN = "yyyyy"

# 1. Récupérer les repos GitHub via gh
result = subprocess.run(
    ["gh", "repo", "list", GITHUB_USER, "--limit", "1000", "--json", "name,url"],
    capture_output=True,
    text=True
)
repos = json.loads(result.stdout)

# 2. Migrer chaque repo
for repo in repos:
    payload = {
        "clone_addr": repo["url"],
        "auth_username": GITHUB_USER,
        "auth_password": GITHUB_TOKEN,
        "repo_name": repo["name"],
        "mirror": False,
        "private": False,
        "issues": True,
        "pull_requests": True,
        "wiki": True,
        "releases": True,
    }
    r = requests.post(
        f"{FORGEJO_URL}/api/v1/repos/migrate",
        headers={"Authorization": f"token {FORGEJO_TOKEN}"},
        json=payload
	#verify=False   # Use this if you are using a self cert on yunohost
    )
    print(repo["name"], r.status_code, r.text)

