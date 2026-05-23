"""
直接测试 pokemon-tools API（不经过 Agent）
用法: python test_tool_api.py
"""
import json, urllib.request


def test_get_pokemon(name="喷火龙"):
    req = urllib.request.Request(
        "http://localhost:8100/tools/get_pokemon_info",
        data=json.dumps({"name": name}).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req).read())


def test_type_effectiveness(type_name="火"):
    req = urllib.request.Request(
        "http://localhost:8100/tools/get_type_effectiveness",
        data=json.dumps({"type_name": type_name}).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req).read())


def test_weakness(name="喷火龙"):
    req = urllib.request.Request(
        "http://localhost:8100/tools/get_pokemon_weakness",
        data=json.dumps({"name": name}).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req).read())


def test_evolution(name="小火龙"):
    req = urllib.request.Request(
        "http://localhost:8100/tools/get_evolution_chain",
        data=json.dumps({"name": name}).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req).read())


if __name__ == "__main__":
    print("=== get_pokemon_info ===")
    print(json.dumps(test_get_pokemon(), ensure_ascii=False, indent=2))
    print("\n=== get_pokemon_weakness ===")
    print(json.dumps(test_weakness(), ensure_ascii=False, indent=2))
