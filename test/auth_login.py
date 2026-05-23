"""
Dify API 认证工具
用法: python auth_login.py
输出 access_token 和 csrf_token
"""
import json, urllib.request, http.cookiejar


def login(email="3775060926@qq.com", password="Z3dienM2NjY="):
    """登录 Dify，返回 (opener, csrf_token)"""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    data = json.dumps({"email": email, "password": password, "remember_me": True}).encode()
    req = urllib.request.Request(
        "http://localhost/console/api/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    opener.open(req)
    csrf = next((c.value for c in cj if c.name == "csrf_token"), None)
    return opener, csrf


if __name__ == "__main__":
    opener, csrf = login()
    print(f"CSRF token: {csrf[:30]}...")
    print("Login successful")
