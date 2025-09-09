import os, requests, json, base64
from llm_utils import llm

GH_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")

def get_plan_comment():
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
    r = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"})
    r.raise_for_status()
    comments = r.json()
    for c in comments[::-1]:  # latest first
        if c["body"].startswith("### 🤖 Autopilot Plan"):
            return c["body"]
    return None

def create_branch(branch_name="autopilot-branch"):
    url = f"https://api.github.com/repos/{REPO}/git/refs/heads/main"
    r = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"})
    r.raise_for_status()
    sha = r.json()["object"]["sha"]

    data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
    url = f"https://api.github.com/repos/{REPO}/git/refs"
    r = requests.post(url, headers={"Authorization": f"token {GH_TOKEN}"}, json=data)
    r.raise_for_status()

def commit_file(branch_name, path, content):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = {
        "message": f"Autopilot update {path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch_name,
    }
    r = requests.put(url, headers={"Authorization": f"token {GH_TOKEN}"}, json=data)
    r.raise_for_status()

def open_pr(branch_name, plan):
    url = f"https://api.github.com/repos/{REPO}/pulls"
    data = {
        "title": f"Autopilot PR for Issue #{ISSUE_NUMBER}",
        "head": branch_name,
        "base": "main",
        "body": plan
    }
    r = requests.post(url, headers={"Authorization": f"token {GH_TOKEN}"}, json=data)
    r.raise_for_status()

if __name__ == "__main__":
    plan = get_plan_comment()
    if not plan:
        raise SystemExit("No plan found on the issue!")

    branch = f"autopilot-{ISSUE_NUMBER}"
    create_branch(branch)
    commit_file(branch, "autopilot.txt", f"Plan:\n\n{plan}")
    open_pr(branch, plan)

