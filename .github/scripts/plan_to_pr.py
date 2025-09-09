import os, re, json, requests
from llm_utils import llm

repo        = os.getenv("GITHUB_REPOSITORY","")
issue_num   = os.getenv("ISSUE_NUMBER","")
issue_title = os.getenv("ISSUE_TITLE","")
gh_token    = os.getenv("GH_TOKEN")
branch      = f"autopilot/issue-{issue_num}"

owner, name = repo.split("/")
API = f"https://api.github.com/repos/{owner}/{name}"
H = {"Authorization":f"Bearer {gh_token}", "Accept":"application/vnd.github+json"}

# 1) Get last plan comment
comments = requests.get(f"{API}/issues/{issue_num}/comments", headers=H).json()
plan = next((c["body"] for c in reversed(comments) if "AUTOPILOT PLAN" in c["body"]), "")

# 2) Generate patch
PROMPT = f"""
Based on this PLAN, generate a minimal patch to start implementing.
Rules:
- Keep diff small (≤ ~100 lines).
- If creating files, include full content.
- Focus on scaffolding first (folders, basic code).
- Use Python or JSON for n8n flow exports when relevant.
PLAN:
{plan}

Output format:
```patch
<unified diff or indicate file writes clearly>
"""
patch = llm(PROMPT)

# Save patch for GitHub Actions job
with open("autopilot.diff","w",encoding="utf-8") as f:
    f.write(patch)

print("::set-output name=patch::autopilot.diff")
print("PR_TITLE::", f"[Autopilot] {issue_title}".replace("\n"," "))
