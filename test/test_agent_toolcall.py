"""
测试 Agent 工具调用
用法: python test_agent_toolcall.py ["查询语句"]

默认查询喷火龙信息，可传参自定义查询。
流式输出关键事件（工具调用、结果、完成）。
"""
import json, urllib.request, sys

API_KEY = "app-MxbH9j4SG861NENYrNf1hRsJ"


def test_agent(query="请使用工具查询喷火龙的详细信息"):
    """发送查询到 Agent，打印工具调用和回答"""
    payload = {
        "inputs": {"user_name": "用户", "assistant_name": "助手"},
        "query": query,
        "response_mode": "streaming",
        "user": "tester",
    }
    req = urllib.request.Request(
        "http://localhost/v1/chat-messages",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=120)
    raw = b""
    for c in resp:
        raw += c
    for line in raw.decode().strip().split("\n"):
        if line.startswith("data: "):
            d = json.loads(line[6:])
            e = d.get("event")
            if e == "agent_thought" and d.get("tool"):
                print(f"[TOOL] {d['tool']}")
            if e == "agent_thought" and d.get("observation"):
                print(f"[OBS] {d['observation'][:200]}")
            if e == "message_end":
                meta = d.get("metadata", {})
                usage = meta.get("usage", {})
                print(f"[DONE] tokens: {usage.get('total_tokens', 'N/A')}")


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "请使用工具查询喷火龙的详细信息"
    test_agent(query)
