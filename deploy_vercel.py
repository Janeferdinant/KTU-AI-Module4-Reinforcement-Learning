import os
import sys
import json
import urllib.request
import urllib.error
import base64

ROOT_DIR = r"c:\Users\Asus\Downloads\AI-MOD4"
PROJECT_NAME = "ktu-ai-module4-rl"

def get_vercel_token():
    auth_path = os.path.expanduser(r"~\AppData\Roaming\com.vercel.cli\auth.json")
    if os.path.exists(auth_path):
        with open(auth_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            token = data.get("token")
            if token:
                print(f"[AUTH] Vercel token retrieved successfully (Length: {len(token)})")
                return token
    print("[AUTH] Error: Vercel token not found in auth.json")
    return None

def build_file_payload():
    files_to_deploy = []

    # 1. Root files
    root_files = ["index.html", "README.md", "vercel.json"]
    for fname in root_files:
        fpath = os.path.join(ROOT_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            files_to_deploy.append({
                "file": fname,
                "data": content,
                "encoding": "utf-8"
            })
            print(f"  + Added text file: {fname} ({len(content)} chars)")

    # 2. Assets directory
    assets_dir = os.path.join(ROOT_DIR, "assets")
    if os.path.exists(assets_dir):
        for fname in sorted(os.listdir(assets_dir)):
            fpath = os.path.join(assets_dir, fname)
            if os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    b64_content = base64.b64encode(f.read()).decode("utf-8")
                files_to_deploy.append({
                    "file": f"assets/{fname}",
                    "data": b64_content,
                    "encoding": "base64"
                })
                print(f"  + Added asset: assets/{fname} ({os.path.getsize(fpath)} bytes)")

    return files_to_deploy

def deploy():
    token = get_vercel_token()
    if not token:
        sys.exit(1)

    files = build_file_payload()
    print(f"\n[DEPLOY] Prepared {len(files)} files for Vercel deployment...")

    deploy_payload = json.dumps({
        "name": PROJECT_NAME,
        "files": files,
        "projectSettings": {
            "framework": None
        },
        "target": "production"
    }).encode("utf-8")

    req = urllib.request.Request("https://api.vercel.com/v13/deployments", data=deploy_payload, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            deployment_url = f"https://{data.get('url')}"
            alias_url = f"https://{PROJECT_NAME}.vercel.app"
            dep_id = data.get('id')
            state = data.get('readyState') or data.get('state')
            print("\n" + "="*60)
            print("VERCEL DEPLOYMENT SUCCESSFUL!")
            print(f"Production URL:  {alias_url}")
            print(f"Deployment URL:  {deployment_url}")
            print(f"Deployment ID:   {dep_id}")
            print(f"Ready State:     {state}")
            print("="*60 + "\n")
            return alias_url
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        print(f"[ERROR] Vercel API Error {e.code}: {err_msg}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Deployment error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
