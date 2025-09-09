import os, json, re
from llm_utils import llm
import requests

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

headers={"Authorization":f"Bearer {gh_token}","Accept":"application/vnd.github+json"}
owner, name = repo.split("/")
api = f"https://api.github.com/repos/{owner}/{name}"

requests.post(f"{api}/issues/{issue_num}/comments",
              headers=headers,json={"body": f"### AUTOPILOT PLAN\n\n{plan}"})

requests.post(f"{api}/issues/{issue_num}/labels",
              headers=headers,json={"labels": ["PLAN_READY"]})

print("Plan posted and PLAN_READY label added.")


