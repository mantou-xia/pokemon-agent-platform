"""Check DeepSeek credentials in database"""
import json, psycopg2, sys
sys.stdout.reconfigure(encoding="utf-8")

conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

# Check provider_credentials
cur.execute("SELECT * FROM provider_credentials WHERE provider_name LIKE '%deepseek%'")
cols = [desc[0] for desc in cur.description]
for row in cur.fetchall():
    print("=== provider_credentials ===")
    for i, name in enumerate(cols):
        print(f"  {name}={row[i]}")
    print()

# Check provider_models
cur.execute("SELECT * FROM provider_models WHERE provider_name LIKE '%deepseek%'")
cols = [desc[0] for desc in cur.description]
for row in cur.fetchall():
    print("=== provider_models ===")
    for i, name in enumerate(cols):
        print(f"  {name}={row[i]}")
    print()

# Check provider_model_credentials
cur.execute("SELECT * FROM provider_model_credentials WHERE provider_name LIKE '%deepseek%'")
cols = [desc[0] for desc in cur.description]
for row in cur.fetchall():
    print("=== provider_model_credentials ===")
    for i, name in enumerate(cols):
        val = str(row[i])[:200] if row[i] else "NULL"
        print(f"  {name}={val}")
    print()

# Check what model the app is using
cur.execute("""
    SELECT id, model FROM app_model_configs
    WHERE app_id = '87ddbbae-b851-4827-97ef-b7e2eeb8d29d'
    ORDER BY created_at DESC LIMIT 1
""")
row = cur.fetchone()
if row:
    print(f"App model config: id={row[0][:8]}... model={row[1][:200]}")

cur.close()
conn.close()
