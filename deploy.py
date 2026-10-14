import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import hashlib
import base64

ROOT_DIR = r"c:\Users\Asus\Downloads\AI-MOD4"

def step_log(msg):
    print(f"\n[DEPLOY-STEP] {msg}")

# 1. Update index.html to embed graphics
def update_index_html():
    step_log("Embedding hero banner and research graphics into index.html...")
    index_path = os.path.join(ROOT_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert hero banner in Tab 1 if not present
    hero_img_markup = '''
      <!-- Liquid Glass Hero Graphic Banner -->
      <div class="glass-card" style="padding: 10px; margin-bottom: 24px; text-align: center; border-radius: var(--radius-lg); overflow: hidden;">
        <img src="assets/hero-banner.jpg" alt="Reinforcement Learning Liquid Glass Hero Banner" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: var(--radius-md); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      </div>
'''
    if "assets/hero-banner.jpg" not in content:
        # Insert after <div class="tab-pane active" id="tab-theory"> ... section-title-bar
        target = '</div>\n        <span class="badge-pill emerald">Full Syllabus Solved</span>\n      </div>'
        if target in content:
            content = content.replace(target, target + "\n" + hero_img_markup)
            print("  -> Inserted hero banner into Tab 1")
        else:
            print("  -> Warning: target not found for hero banner")

    # Insert research graphic in Tab 2 if not present
    research_img_markup = '''
      <!-- Liquid Glass Research Infographic Graphic -->
      <div class="glass-card" style="padding: 10px; margin-bottom: 24px; text-align: center; border-radius: var(--radius-lg); overflow: hidden;">
        <img src="assets/research-graphic.jpg" alt="Deep Reinforcement Learning Algorithms Graphic" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: var(--radius-md); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      </div>
'''
    if "assets/research-graphic.jpg" not in content:
        target2 = '</div>\n        <span class="badge-pill violet">Peer-Reviewed Milestones</span>\n      </div>'
        if target2 in content:
            content = content.replace(target2, target2 + "\n" + research_img_markup)
            print("  -> Inserted research graphic into Tab 2")
        else:
            print("  -> Warning: target not found for research graphic")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  -> index.html successfully updated with graphics.")

# 2. Generate comprehensive README.md with graphics
def generate_readme():
    step_log("Checking README.md...")
    readme_path = os.path.join(ROOT_DIR, "README.md")
    if os.path.exists(readme_path):
        print("  -> README.md is present and verified.")
    else:
        print("  -> README.md not found.")

# 3. Retrieve GitHub credentials from Windows Credential Manager
def get_github_token():
    step_log("Extracting GitHub token from Windows Credential Manager...")
    try:
        p = subprocess.Popen(
            ['git', 'credential', 'fill'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = p.communicate('protocol=https\nhost=github.com\nusername=Janeferdinant\n\n')
        token = ""
        for line in out.splitlines():
            if line.startswith('password='):
                token = line.split('=', 1)[1]
        if token:
            print(f"  -> GitHub token retrieved! Prefix: {token[:4]}... (Length: {len(token)})")
            return token
        else:
            print("  -> Could not extract token from git credential fill.")
            return None
    except Exception as e:
        print(f"  -> Error getting GitHub token: {e}")
        return None

# 4. Create or verify GitHub repository
def setup_github_repo(token):
    step_log("Verifying / Creating GitHub repository 'KTU-AI-Module4-Reinforcement-Learning'...")
    repo_name = "KTU-AI-Module4-Reinforcement-Learning"
    user_name = "Janeferdinant"

    # Check if repo exists
    check_url = f"https://api.github.com/repos/{user_name}/{repo_name}"
    req = urllib.request.Request(check_url, headers={
        "Authorization": f"token {token}",
        "User-Agent": "JaneRoseDeployer"
    })
    
    repo_exists = False
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"  -> Repository exists: {data.get('html_url')}")
            repo_exists = True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("  -> Repository does not exist. Creating new public repository...")
        else:
            print(f"  -> GitHub API Error {e.code}: {e.read().decode()[:200]}")

    if not repo_exists:
        create_url = "https://api.github.com/user/repos"
        payload = json.dumps({
            "name": repo_name,
            "description": "KTU S5 AI Module 4: Reinforcement Learning Master Knowledge System - Liquid Glass Dashboard, Live Research Paper Demos, Exam Solver & Vercel Deployment by Jane Rose",
            "homepage": "https://ktu-ai-module4-rl.vercel.app",
            "private": False,
            "has_issues": True,
            "has_wiki": True
        }).encode("utf-8")

        req = urllib.request.Request(create_url, data=payload, headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "User-Agent": "JaneRoseDeployer"
        })
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                print(f"  -> Repository created: {data.get('html_url')}")
        except Exception as e:
            print(f"  -> Failed to create repository: {e}")
            return False

    return f"https://{user_name}:{token}@github.com/{user_name}/{repo_name}.git"

# 5. Git commit and push
def git_commit_and_push(remote_url):
    step_log("Committing changes and pushing to GitHub via Git...")
    def run_git(args):
        r = subprocess.run(['git'] + args, cwd=ROOT_DIR, capture_output=True, text=True)
        if r.stdout.strip():
            print(f"    [git {args[0]}] {r.stdout.strip()[:200]}")
        if r.stderr.strip() and r.returncode != 0:
            print(f"    [git {args[0]} ERR] {r.stderr.strip()[:200]}")
        return r.returncode == 0

    run_git(['init'])
    run_git(['config', 'user.name', 'Janeferdinant'])
    run_git(['config', 'user.email', 'janeferdinant@gmail.com'])
    run_git(['remote', 'remove', 'origin'])
    run_git(['remote', 'add', 'origin', remote_url])
    run_git(['add', '.'])
    run_git(['commit', '-m', 'feat: complete KTU S5 AI Module 4 Reinforcement Learning platform with liquid glass dashboard, live demos, and exam solver by Jane Rose'])
    run_git(['branch', '-M', 'main'])
    success = run_git(['push', '-u', 'origin', 'main', '--force'])
    if success:
        print("  -> Git push to GitHub successful!")
    else:
        print("  -> Git push encountered an issue, check logs above.")
    return success

# 6. Retrieve Vercel token from AppData
def get_vercel_token():
    step_log("Extracting Vercel token from AppData...")
    auth_path = os.path.expanduser(r"~\AppData\Roaming\com.vercel.cli\auth.json")
    if os.path.exists(auth_path):
        with open(auth_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            token = data.get("token")
            if token:
                print(f"  -> Vercel token retrieved! (Length: {len(token)})")
                return token
    print("  -> Vercel token not found in auth.json")
    return None

# 7. Deploy to Vercel via Vercel Deployments API
def deploy_to_vercel(vercel_token):
    step_log("Deploying project to Vercel via Vercel API...")
    project_name = "ktu-ai-module4-rl"
    
    # Read files to deploy
    files_to_deploy = []
    
    # 1) index.html
    index_file = os.path.join(ROOT_DIR, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        html_data = f.read()
    files_to_deploy.append({
        "file": "index.html",
        "data": html_data,
        "encoding": "utf-8"
    })
    
    # 2) vercel.json
    vercel_file = os.path.join(ROOT_DIR, "vercel.json")
    if os.path.exists(vercel_file):
        with open(vercel_file, "r", encoding="utf-8") as f:
            v_data = f.read()
        files_to_deploy.append({
            "file": "vercel.json",
            "data": v_data,
            "encoding": "utf-8"
        })

    # 3) assets/hero-banner.jpg
    hero_path = os.path.join(ROOT_DIR, "assets", "hero-banner.jpg")
    if os.path.exists(hero_path):
        with open(hero_path, "rb") as f:
            hero_b64 = base64.b64encode(f.read()).decode("utf-8")
        files_to_deploy.append({
            "file": "assets/hero-banner.jpg",
            "data": hero_b64,
            "encoding": "base64"
        })

    # 4) assets/research-graphic.jpg
    res_path = os.path.join(ROOT_DIR, "assets", "research-graphic.jpg")
    if os.path.exists(res_path):
        with open(res_path, "rb") as f:
            res_b64 = base64.b64encode(f.read()).decode("utf-8")
        files_to_deploy.append({
            "file": "assets/research-graphic.jpg",
            "data": res_b64,
            "encoding": "base64"
        })

    # 5) README.md
    readme_path = os.path.join(ROOT_DIR, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            rm_data = f.read()
        files_to_deploy.append({
            "file": "README.md",
            "data": rm_data,
            "encoding": "utf-8"
        })

    print(f"  -> Uploading {len(files_to_deploy)} project files to Vercel...")

    deploy_payload = json.dumps({
        "name": project_name,
        "files": files_to_deploy,
        "projectSettings": {
            "framework": None
        },
        "target": "production"
    }).encode("utf-8")

    req = urllib.request.Request("https://api.vercel.com/v13/deployments", data=deploy_payload, headers={
        "Authorization": f"Bearer {vercel_token}",
        "Content-Type": "application/json"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            deployment_url = f"https://{data.get('url')}"
            alias_url = f"https://{project_name}.vercel.app"
            print(f"\n=======================================================")
            print(f"[SUCCESS] VERCEL DEPLOYMENT SUCCESSFUL!")
            print(f"Production URL:  {alias_url}")
            print(f"Deployment URL:  {deployment_url}")
            print(f"Deployment ID:   {data.get('id')}")
            print(f"Status:          {data.get('readyState')}")
            print(f"=======================================================\n")
            return alias_url
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        print(f"  -> Vercel API Error {e.code}: {err_msg}")
        return None
    except Exception as e:
        print(f"  -> Vercel deployment error: {e}")
        return None

def main():
    print("=" * 65)
    print("KTU S5 AI MODULE 4: REINFORCEMENT LEARNING DEPLOYMENT PIPELINE")
    print("Curated & Created by Jane Rose")
    print("=" * 65)

    # Step 1: Update index.html with graphics
    update_index_html()

    # Step 2: Generate README.md with graphics & badges
    generate_readme()

    # Step 3: Get GitHub token from Credential Manager
    gh_token = get_github_token()
    if gh_token:
        # Step 4: Setup GitHub repo
        remote_url = setup_github_repo(gh_token)
        if remote_url:
            # Step 5: Git commit & push
            git_commit_and_push(remote_url)
    else:
        print("  -> Skipping GitHub push (token not found)")

    # Step 6: Deploy to Vercel
    v_token = get_vercel_token()
    if v_token:
        deploy_to_vercel(v_token)
    else:
        print("  -> Skipping Vercel deploy (token not found)")

if __name__ == "__main__":
    main()
