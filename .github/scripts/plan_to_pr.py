import os, json, re
from llm_utils import llm

issue_title = os.getenv("ISSUE_TITLE","")
issue_body  = os.getenv("ISSUE_BODY","")
repo        = os.getenv("GITHUB_REPOSITORY","")
issue_num   = os.getenv("ISSUE_NUMBER","")
gh_token    = os.getenv("GH_TOKEN")

PLAN_PROMPT = f"""
You are the repo's project architect. From this issue, produce:

1) PLAN: bullet list of minimal steps to implement (≤10 bullets).
2) FILES: list of files to add/change with short rationale.
3) TESTS: quick checks we will run in CI.
4) ACCEPTANCE: Done criteria in 3-5 lines.

Issue Title: {issue_title}
Issue Body:
{issue_body}

Keep output under 400 tokens. Use repo-friendly language.
"""

plan = llm(PLAN_PROMPT)

# Post plan as a comment + add label PLAN_READY
import requests
headers={"Authorization":f"Bearer {gh_token}","Accept":"application/vnd.github+json"}
owner, name = repo.split("/")
api = f"https://api.github.com/repos/{owner}/{name}"

requests.post(f"{api}/issues/{issue_num}/comments",
              headers=headers,json={"body": f"### AUTOPILOT PLAN\n\n{plan}"})

requests.post(f"{api}/issues/{issue_num}/labels",
              headers=headers,json={"labels": ["PLAN_READY"]})
print("Plan posted and PLAN_READY label added.")
C)
.github/scripts/plan_to_pr.py
import os, re, json, base64, requests
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

# 2) Ask LLM to produce a small patch (unified diff or explicit file writes)
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
