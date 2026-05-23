# Phase 2 执行流程（可复现 SOP）

本文件记录从启动到完成 Agent 工具调用验证的完整流程。
后续 Agent 遇到 Phase 2 相关任务时，直接按此流程执行，无需重新思考。

---

## A. 启动环境

### A1. 检查 Docker Desktop
```bash
docker info --format '{{.ServerVersion}}'
# 必须显示版本号，如 29.4.3
```

### A2. 确认 Dify 容器已运行
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
# 关键：docker-nginx-1, docker-api-1(healthy), docker-db_postgres-1(healthy)
```

**可能的问题**：
- 如果两套容器（`dify-*` 和 `docker-*`）同时存在：
  ```bash
  docker compose -p dify down  # 停掉冗余的 dify 项目
  ```
- 如果 API 返回 502（nginx 缓存旧 IP）：
  ```bash
  docker restart docker-nginx-1
  ```

### A3. 确认 Pokemon Tools API 在运行
```bash
curl -s http://localhost:8100/health
# 期望：{"status":"ok"}
```
如果未运行：
```bash
python "d:\git depository\pokemon-agent-platform\plugins\pokemon-tools\main.py" &
```

### A4. 确认 Ollama 及模型
```bash
curl -s http://localhost:11434/api/tags
# 期望：models 列表中有 deepseek-r1:8b（或其他可用模型）
```

> ⚠️ 如果模型崩溃（"llama runner process has terminated"）：
> 1. 检查 C 盘空间，可能需要清理后重启
> 2. 或切换更小模型：`ollama pull qwen2:1.5b`
> 3. 切换后需要在 Dify Studio 中更新 Agent 的模型配置

---

## B. Dify API 认证

### B1. 登录获取 cookies

```bash
# 密码需 Base64 编码（Dify 的 FieldEncryption 仅做 Base64，不做 RSA）
# python -c "import base64; print(base64.b64encode(b'gwbzs666').decode())"
# → Z3dienM2NjY=

curl -sv -X POST "http://localhost/console/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"3775060926@qq.com","password":"Z3dienM2NjY=","remember_me":true}' \
  -c cookies.txt
```

响应中 Set-Cookie 包含：
- `access_token`（JWT，1小时有效期）
- `csrf_token`（1小时有效期，用于后续 API 调用）

### B2. 验证认证状态

```bash
# 需要同时带 cookie 和 X-CSRF-TOKEN header
CSRF_TOKEN="<从 cookies.txt 获取 csrf_token 的值>"
curl -s -b cookies.txt \
  -H "X-CSRF-TOKEN: $CSRF_TOKEN" \
  "http://localhost/console/api/apps?page=1&limit=20"
```

---

## C. 工具接入状态（已确认）

**已有应用**："Pokemon助手" (agent-chat mode)
- 应用 ID: `87ddbbae-b851-4827-97ef-b7e2eeb8d29d`
- 已配置模型：`deepseek-r1:8b`（通过 Ollama）
- **已将 pokemon-tools 的 8 个工具全部导入并启用**：
  1. `get_pokemon_info` - 获取宝可梦详细信息
  2. `get_pokemon_weakness` - 获取宝可梦弱点
  3. `get_type_effectiveness` - 查询属性克制关系
  4. `get_evolution_chain` - 获取宝可梦进化链
  5. `list_tools` - 列出所有可用工具
  6. `health` - 健康检查
  7. `get_openapi_yaml/yml` - 获取 OpenAPI 描述文件

**已确认**：Dify API 容器内部可访问 `host.docker.internal:8100`（网络连通性通过）

---

## D. 创建 API Key 并测试

### D1. 创建 API Key（如不存在）

```bash
CSRF_TOKEN="<token>"
curl -s -X POST -b cookies.txt \
  -H "X-CSRF-TOKEN: $CSRF_TOKEN" \
  "http://localhost/console/api/apps/87ddbbae-b851-4827-97ef-b7e2eeb8d29d/api-keys"
```

响应包含 `token` 字段，如 `app-MxbH9j4SG861NENYrNf1hRsJ`

### D2. 发送测试消息（streaming 模式）

```bash
# Agent Chat 不支持 blocking 模式，必须用 streaming
API_KEY="app-xxx"
curl -s -X POST "http://localhost/v1/chat-messages" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {"user_name":"测试用户","assistant_name":"宝可梦助手"},
    "query":"喷火龙是什么属性的宝可梦？请调用工具查询。",
    "response_mode":"streaming",
    "user":"test-user-01"
  }'
```

### D3. 期望的响应流

```
data: {"event":"agent_thought", ...}  # Agent 开始思考
data: {"event":"agent_thought", ..., "tool":"get_pokemon_info", "tool_input":"...", "observation":"..."}  # 调用工具
data: {"event":"message", ..., "answer":"喷火龙是火属性和飞行属性的宝可梦..."}  # 最终回答
data: {"event":"message_end", ...}
```

**常见错误**：
- `{"error":"llama runner process has terminated"}` → Ollama 模型无法加载（C盘/内存不足）
- `"access_token is invalid"` → API Key 不对，检查是否已创建
- `"Agent Chat App does not support blocking mode"` → 必须用 streaming

---

## E. 网络拓扑（为什么是 host.docker.internal:8100）

```
User
│
▼
Dify Web (nginx:80) → Dify API (api:5001) → Ollama (host.docker.internal:11434)
                                               │
                                               ▼
                                        pokemon-tools (host.docker.internal:8100)
                                               │
                                               ▼
                                        PostgreSQL (host.docker.internal:5432)
```

- pokemon-tools 运行在主机的 Python 进程中（不在 Docker 内）
- Dify 容器通过 `host.docker.internal` 访问主机的 pokemon-tools
- pokemon-tools 通过 `localhost:5432` 连接 Dify 的 PostgreSQL（已暴露 5432 端口）

---

## F. 已知限制

1. **模型依赖**：Agent 调用工具需要 LLM 正常工作。当前只有 `deepseek-r1:8b`，
   需要约 8GB 可用 RAM 和足够的磁盘空间。
2. **API 有效期**：Dify 的 access_token 和 csrf_token 有效期 1 小时，
   长时间任务需要更新 cookie。
3. **工具参数**：当前工具参数（`name`, `type_name`）未设置默认值，
   Agent 需自行推断参数值。
4. **Dify 版本**：当前部署版本为 1.14.2。
