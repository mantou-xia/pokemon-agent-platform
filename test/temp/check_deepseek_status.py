"""Check DeepSeek provider status in Dify"""
import json, urllib.request, http.cookiejar, sys
sys.stdout.reconfigure(encoding="utf-8")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

data = json.dumps({"email": "3775060926@qq.com", "password": "Z3dienM2NjY=", "remember_me": True}).encode()
req = urllib.request.Request("http://localhost/console/api/login", data=data, headers={"Content-Type": "application/json"})
opener.open(req)
csrf = next((c.value for c in cj if c.name == "csrf_token"), None)

# Check provider status
req = urllib.request.Request("http://localhost/console/api/workspaces/current/model-providers")
req.add_header("X-CSRF-TOKEN", csrf)
resp = opener.open(req)
data = json.loads(resp.read())

for p in data.get("data", []):
    if "deepseek" in p.get("provider", "").lower():
        print(f"Provider: {p['provider']}")
        print(f"  config methods: {p.get('configurate_methods')}")
        models = p.get("models", [])
        print(f"  models: {json.dumps(models, ensure_ascii=False)[:2000]}")
        print()
