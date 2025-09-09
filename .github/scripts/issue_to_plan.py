import os, requests, json
from llm_utils import llm

GH_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")

def get_issue_body():
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}"
    r = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"})
    r.raise_for_status()
    return r.json()["body"]

def post_plan(plan: str):
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
    body = {"body": f"### 🤖 Autopilot Plan\n\n{plan}"}
    r = requests.post(url, headers={"Authorization": f"token {GH_TOKEN}"}, json=body)
    r.raise_for_status()

if __name__ == "__main__":
    issue_text = get_issue_body()
    plan = llm(f"Create a concise, actionable implementation plan for this GitHub issue:\n\n{issue_text}")
    post_plan(plan)

