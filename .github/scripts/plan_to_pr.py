import os, re, requests, sys
from llm_utils import llm

repo        = os.getenv("GITHUB_REPOSITORY", "")
issue_num   = os.getenv("ISSUE_NUMBER", "")
issue_title = os.getenv("ISSUE_TITLE", "")
gh_token    = os.getenv("GH_TOKEN")
branch      = f"autopilot/issue-{issue_num}"

if not repo or not issue_num or not gh_token:
    print("❌ Missing required environment variables")
    sys.exit(1)

owner, name = repo.split("/")
API = f"https://api.github.com/repos/{owner}/{name}"
H = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}

# 1) Get last plan comment
comments = requests.get(f"{API}/issues/{issue_num}/comments", headers=H)
comments.raise_for_status()
comments = comments.json()
plan = next((c["body"] for c in reversed(comments) if "AUTOPILOT PLAN" in c["body"]), "")

if not plan:
    print("❌ No plan found in comments. Exiting.")
    sys.exit(1)

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
```"""

patch = llm(PROMPT)

# --- Clean patch output ---
patch_clean = re.sub(r"^```(?:patch)?", "", patch.strip(), flags=re.MULTILINE)
patch_clean = re.sub(r"```$", "", patch_clean.strip(), flags=re.MULTILINE)

# Save patch for GitHub Actions job
with open("autopilot.diff", "w", encoding="utf-8") as f:
    f.write(patch_clean.strip() + "\n")

# 3) Export outputs (modern GitHub Actions way)
with open(os.getenv("GITHUB_OUTPUT"), "a", encoding="utf-8") as gh_out:
    gh_out.write(f"patch=autopilot.diff\n")
    gh_out.write(f"title=[Autopilot] {issue_title.replace(chr(10), ' ')}\n")

print("✅ Patch generated successfully")
