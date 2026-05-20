"""
Pokemon Tools API for Dify Agent
Provides deterministic Pokemon tools for Dify Agent function calling.

Usage:
    python main.py
    # Runs on http://localhost:8100
"""

import os
import json
from pathlib import Path

import psycopg2
import psycopg2.extras
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Pokemon Tools", version="1.0.0", servers=[{"url": "http://host.docker.internal:8100", "description": "Pokemon Tools 本地服务"}])

# --- Request Schemas ---
class NameRequest(BaseModel):
    name: str

class TypeRequest(BaseModel):
    type_name: str


# --- Database ---

# Serve the OpenAPI yaml file for manual import
BASE_DIR = Path(__file__).parent

@app.get("/openapi.yaml")
def get_openapi_yaml():
    return FileResponse(BASE_DIR / "openapi.yaml", media_type="text/yaml")

@app.get("/openapi.yml")
def get_openapi_yml():
    return FileResponse(BASE_DIR / "openapi.yaml", media_type="text/yaml")

# Database connection (uses Dify's existing PostgreSQL)
DB_URL = os.getenv("POKEMON_DB_URL", "host=localhost port=5432 dbname=dify user=postgres password=difyai123456")


def get_db():
    """Get database connection."""
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    return conn


@app.get("/tools")
def list_tools():
    """List all available tools (for Dify OpenAPI spec)."""
    return {
        "tools": [
            {
                "name": "get_pokemon_info",
                "description": "Get detailed information about a Pokemon by its Chinese or English name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Pokemon name in Chinese or English"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_type_effectiveness",
                "description": "Get type effectiveness info: which types are strong/weak against the given type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type_name": {
                            "type": "string",
                            "description": "Type name in Chinese, e.g. 火, 水, 草"
                        }
                    },
                    "required": ["type_name"]
                }
            },
            {
                "name": "get_pokemon_weakness",
                "description": "Get all weaknesses of a Pokemon by its name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Pokemon name in Chinese or English"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_evolution_chain",
                "description": "Get the evolution chain of a Pokemon",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Pokemon name in Chinese or English"
                        }
                    },
                    "required": ["name"]
                }
            }
        ]
    }


@app.post("/tools/get_pokemon_info")
def tool_get_pokemon_info(req: NameRequest):
    """获取宝可梦详细信息。根据中文或英文名查询，返回属性、种族值、描述等。"""
    name = req.name

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT p.*, t1.name_zh as type1_zh, t1.name_en as type1_en, "
        "t2.name_zh as type2_zh, t2.name_en as type2_en "
        "FROM pokemon p "
        "LEFT JOIN pokemon_types t1 ON p.type1_id = t1.id "
        "LEFT JOIN pokemon_types t2 ON p.type2_id = t2.id "
        "WHERE p.name_zh = %s OR p.name_en = %s OR LOWER(p.name_en) = LOWER(%s)",
        (name, name, name)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")

    result = dict(row)
    # Clean up datetime objects for JSON
    for k, v in result.items():
        if hasattr(v, 'isoformat'):
            result[k] = v.isoformat()

    return {
        "national_id": result["national_id"],
        "name_zh": result["name_zh"],
        "name_en": result["name_en"],
        "type1": result["type1_zh"] or "",
        "type2": result["type2_zh"] or "",
        "stats": {
            "hp": result["hp"],
            "attack": result["attack"],
            "defense": result["defense"],
            "sp_attack": result["sp_attack"],
            "sp_defense": result["sp_defense"],
            "speed": result["speed"],
            "total": result["hp"] + result["attack"] + result["defense"] + result["sp_attack"] + result["sp_defense"] + result["speed"]
        },
        "description": result.get("description", "")
    }


@app.post("/tools/get_pokemon_weakness")
def tool_get_pokemon_weakness(req: NameRequest):
    """获取宝可梦弱点。查询指定宝可梦被什么属性克制。"""
    name = req.name

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # First get the Pokemon
    cur.execute("SELECT national_id, name_zh, name_en, type1_id, type2_id FROM pokemon WHERE name_zh = %s OR name_en = %s OR LOWER(name_en) = LOWER(%s)", (name, name, name))
    poke = cur.fetchone()
    if not poke:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")

    # Get weaknesses
    cur.execute("""
        SELECT te_att.name_zh AS type, te.multiplier
        FROM pokemon p
        JOIN type_effectiveness te ON te.defending_type_id IN (p.type1_id)
        JOIN pokemon_types te_att ON te.attacking_type_id = te_att.id
        WHERE p.national_id = %s AND te.multiplier > 1.0
        UNION
        SELECT te_att.name_zh, te.multiplier
        FROM pokemon p
        JOIN type_effectiveness te ON te.defending_type_id = p.type2_id
        JOIN pokemon_types te_att ON te.attacking_type_id = te_att.id
        WHERE p.national_id = %s AND te.multiplier > 1.0 AND p.type2_id IS NOT NULL
        ORDER BY multiplier DESC
    """, (poke["national_id"], poke["national_id"]))

    weaknesses = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "pokemon": poke["name_zh"],
        "weaknesses": [{"type": w["type"], "multiplier": float(w["multiplier"])} for w in weaknesses]
    }


@app.post("/tools/get_type_effectiveness")
def tool_get_type_effectiveness(req: TypeRequest):
    """查询属性克制关系。返回指定属性攻击各属性的效果（2倍/0.5倍/无效）。"""
    type_name = req.type_name

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT d.name_zh AS defending_type, te.multiplier
        FROM type_effectiveness te
        JOIN pokemon_types a ON te.attacking_type_id = a.id
        JOIN pokemon_types d ON te.defending_type_id = d.id
        WHERE a.name_zh = %s
        ORDER BY te.multiplier DESC
    """, (type_name,))
    results = cur.fetchall()
    cur.close()
    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail=f"Type '{type_name}' not found")

    strong = [r["defending_type"] for r in results if r["multiplier"] >= 2.0]
    weak = [r["defending_type"] for r in results if r["multiplier"] <= 0.5 and r["multiplier"] > 0]
    no_effect = [r["defending_type"] for r in results if r["multiplier"] == 0]

    return {
        "type": type_name,
        "strong_against": strong,
        "weak_against": weak,
        "no_effect_against": no_effect
    }


@app.post("/tools/get_evolution_chain")
def tool_get_evolution_chain(req: NameRequest):
    """获取宝可梦进化链。查询指定宝可梦的完整进化路径。"""
    name = req.name

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Find the base form
    cur.execute("""
        WITH RECURSIVE chain AS (
            SELECT p.national_id, p.name_zh, p.name_en, p.evolves_from, 0 AS depth
            FROM pokemon p
            WHERE p.name_zh = %s OR p.name_en = %s OR LOWER(p.name_en) = LOWER(%s)
            UNION
            SELECT p.national_id, p.name_zh, p.name_en, p.evolves_from, c.depth - 1
            FROM pokemon p
            JOIN chain c ON p.national_id = c.evolves_from
        )
        SELECT * FROM chain ORDER BY depth LIMIT 1
    """, (name, name, name))

    base = cur.fetchone()
    if not base:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")

    # Get the base form
    base_id = base["national_id"]
    cur.execute("SELECT national_id FROM pokemon WHERE evolves_from IS NULL AND national_id = %s", (base_id,))
    if not cur.fetchone():
        cur.execute("SELECT evolves_from FROM pokemon WHERE national_id = %s", (base_id,))
        root = cur.fetchone()
        if root and root["evolves_from"]:
            base_id = root["evolves_from"]

    # Get full chain from base
    cur.execute("""
        WITH RECURSIVE chain AS (
            SELECT p.national_id, p.name_zh, p.name_en, p.evolves_from, ec.trigger_method, ec.trigger_detail, 0 AS stage
            FROM pokemon p
            LEFT JOIN evolution_chains ec ON p.national_id = ec.pokemon_id
            WHERE p.evolves_from IS NULL AND p.national_id = %s
            UNION
            SELECT p.national_id, p.name_zh, p.name_en, p.evolves_from, ec.trigger_method, ec.trigger_detail, c.stage + 1
            FROM pokemon p
            JOIN chain c ON p.evolves_from = c.national_id
            LEFT JOIN evolution_chains ec ON p.national_id = ec.pokemon_id
        )
        SELECT * FROM chain ORDER BY stage
    """, (base_id,))

    chain = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "pokemon": name,
        "chain": [
            {
                "name_zh": c["name_zh"],
                "name_en": c["name_en"],
                "trigger": c["trigger_method"],
                "trigger_detail": c["trigger_detail"],
                "stage": c["stage"]
            }
            for c in chain
        ]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
