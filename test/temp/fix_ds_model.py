"""Fix: switch app to DeepSeek and add model"""
import json, psycopg2, uuid, sys
sys.stdout.reconfigure(encoding="utf-8")

conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
tenant_id = "1e4938b2-235f-48eb-b2c8-252cbf6d4c76"
now = "2026-05-23 02:50:00"

# 1) Add deepseek-chat model to provider_models
cur.execute("""SELECT id FROM provider_models 
    WHERE provider_name = 'langgenius/deepseek/deepseek' AND model_name = 'deepseek-chat'""")
if not cur.fetchone():
    mid = str(uuid.uuid4())
    cur.execute("""INSERT INTO provider_models (id, tenant_id, provider_name, model_name, model_type, is_valid, created_at, updated_at)
        VALUES (%s, %s, 'langgenius/deepseek/deepseek', 'deepseek-chat', 'llm', true, %s, %s)""",
        (mid, tenant_id, now, now))
    print("Added deepseek-chat to provider_models")

# 2) Switch app model config to DeepSeek
cur.execute("""SELECT id FROM app_model_configs 
    WHERE app_id = '87ddbbae-b851-4827-97ef-b7e2eeb8d29d' 
    ORDER BY created_at DESC LIMIT 1""")
config_id = cur.fetchone()[0]

new_model = json.dumps({
    "provider": "langgenius/deepseek/deepseek",
    "name": "deepseek-chat",
    "mode": "chat",
    "completion_params": {"stop": []}
})
cur.execute("UPDATE app_model_configs SET model = %s WHERE id = %s", (new_model, config_id))
print(f"Switched app model config {config_id[:8]}... to deepseek-chat")

# 3) Verify
cur.execute("""SELECT model FROM app_model_configs WHERE id = %s""", (config_id,))
m = json.loads(cur.fetchone()[0])
print(f"Verified: provider={m['provider']}, model={m['name']}")

conn.commit()
cur.close()
conn.close()
