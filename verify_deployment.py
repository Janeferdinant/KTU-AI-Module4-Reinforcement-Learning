import urllib.request
import ssl
import sys

ctx = ssl.create_default_context()
urls = [
    ("Dashboard App", "https://ktu-ai-module4-rl.vercel.app"),
    ("RL Loop GIF", "https://ktu-ai-module4-rl.vercel.app/assets/rl_agent_loop.gif"),
    ("Cliff Walking GIF", "https://ktu-ai-module4-rl.vercel.app/assets/cliff_walking_demo.gif"),
    ("Trading Agent GIF", "https://ktu-ai-module4-rl.vercel.app/assets/trading_agent_live.gif"),
    ("Traffic Control GIF", "https://ktu-ai-module4-rl.vercel.app/assets/traffic_control_live.gif"),
    ("Hero Banner JPG", "https://ktu-ai-module4-rl.vercel.app/assets/hero-banner.jpg"),
    ("Research Infographic JPG", "https://ktu-ai-module4-rl.vercel.app/assets/research-graphic.jpg"),
    ("README on Vercel", "https://ktu-ai-module4-rl.vercel.app/README.md"),
    ("README on GitHub", "https://raw.githubusercontent.com/Janeferdinant/KTU-AI-Module4-Reinforcement-Learning/main/README.md")
]

print("=" * 70)
print("VERIFICATION CHECK: PRODUCTION DEPLOYMENTS & ASSETS")
print("=" * 70)

all_ok = True
for label, u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = resp.read()
            code = resp.getcode()
            ct = resp.headers.get("Content-Type")
            print(f"[PASS {code}] {label:20} -> {len(data):,} bytes ({ct}) | {u}")
    except Exception as e:
        print(f"[FAIL]     {label:20} -> Error: {e} | {u}")
        all_ok = False

print("=" * 70)
if all_ok:
    print("ALL 9 PRODUCTION ENDPOINTS RETURNED HTTP 200 OK WITH VALID ASSETS!")
else:
    print("SOME CHECKS FAILED!")
print("=" * 70)
