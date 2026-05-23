"""
通过数据库管理 Dify 模型（添加、切换）

用法:
  python db_model_manager.py list              # 列出 Ollama 模型
  python db_model_manager.py add <model_name>   # 注册新模型
  python db_model_manager.py switch <model_name> # 切换 Agent 模型
"""
import json, psycopg2, uuid, sys

TENANT_ID = "1e4938b2-235f-48eb-b2c8-252cbf6d4c76"
APP_ID = "87ddbbae-b851-4827-97ef-b7e2eeb8d29d"
DB_URL = "host=127.0.0.1 port=5432 dbname=dify user=postgres password=difyai123456"


def get_conn():
    return psycopg2.connect(DB_URL)


def list_models():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT model_name, is_valid FROM provider_models
           WHERE provider_name = 'langgenius/ollama/ollama' ORDER BY model_name"""
    )
    for r in cur.fetchall():
        print(f"  {r[0]} {'[active]' if r[1] else '[inactive]'}")
    cur.close()
    conn.close()


def add_model(model_name):
    conn = get_conn()
    cur = conn.cursor()
    now = "2026-05-22 03:30:00"

    # provider_models
    mid = str(uuid.uuid4())
    cur.execute(
        """INSERT INTO provider_models (id, tenant_id, provider_name, model_name, model_type, is_valid, created_at, updated_at)
           VALUES (%s, %s, 'langgenius/ollama/ollama', %s, 'llm', true, %s, %s)
           ON CONFLICT DO NOTHING""",
        (mid, TENANT_ID, model_name, now, now),
    )

    # credentials (copy deepseek config)
    cid = str(uuid.uuid4())
    config = json.dumps({
        "base_url": "http://host.docker.internal:11434",
        "mode": "chat",
        "context_size": "32768",
        "max_tokens": "8192",
        "vision_support": "false",
        "function_calling_type": "tool_call",
    })
    cur.execute(
        """INSERT INTO provider_model_credentials (id, tenant_id, provider_name, model_name, model_type, encrypted_config, credential_name, created_at, updated_at)
           VALUES (%s, %s, 'langgenius/ollama/ollama', %s, 'llm', %s, 'API KEY 1', %s, %s)
           ON CONFLICT DO NOTHING""",
        (cid, TENANT_ID, model_name, config, now, now),
    )

    cur.execute("UPDATE provider_models SET credential_id = %s WHERE id = %s", (cid, mid))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Added model '{model_name}'")


def switch_model(model_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, model FROM app_model_configs
           WHERE app_id = %s ORDER BY created_at DESC LIMIT 1""",
        (APP_ID,),
    )
    config_id, model_json = cur.fetchone()
    model_data = json.loads(model_json)
    old_name = model_data.get("name", "")
    model_data["name"] = model_name
    cur.execute("UPDATE app_model_configs SET model = %s WHERE id = %s", (json.dumps(model_data), config_id))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Switched model from '{old_name}' to '{model_name}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db_model_manager.py [list|add <name>|switch <name>]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "list":
        list_models()
    elif cmd == "add" and len(sys.argv) >= 3:
        add_model(sys.argv[2])
    elif cmd == "switch" and len(sys.argv) >= 3:
        switch_model(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
