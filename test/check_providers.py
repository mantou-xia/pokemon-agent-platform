"""
查看 Dify 模型提供商信息
用法: python check_providers.py [provider_keyword]

不传参则列出所有提供商；传参可过滤（如 deepseek、ollama）
"""
import json, urllib.request, http.cookiejar, sys
sys.stdout.reconfigure(encoding="utf-8")

from auth_login import login


def list_providers(keyword=None):
    opener, csrf = login()
    req = urllib.request.Request("http://localhost/console/api/workspaces/current/model-providers")
    req.add_header("X-CSRF-TOKEN", csrf)
    resp = opener.open(req)
    data = json.loads(resp.read())

    for p in data.get("data", []):
        name = p.get("provider", "")
        if keyword and keyword.lower() not in name.lower():
            continue
        print(f"\n=== {name} ===")
        print(f"  config_methods: {p.get('configurate_methods')}")
        models = p.get("models", [])
        for m in models:
            print(f"  Model: {m.get('model')}")
        cred = p.get("provider_credential_schema", {})
        for schema in cred.get("credential_form_schemas", []):
            print(f"  Required: {schema.get('variable')} ({schema.get('label', {}).get('zh_Hans', schema.get('label', {}).get('en_US', ''))})")


if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    list_providers(kw)
