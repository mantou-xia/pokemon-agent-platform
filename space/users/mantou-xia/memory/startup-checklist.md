# 启动清单

每次重新打开电脑后，按以下顺序启动所有服务。

---

## 1. 启动 Docker Desktop

确保 Docker Desktop 已运行（托盘图标变绿）。

验证：
```bash
docker info --format '{{.ServerVersion}}'
# ✅ 显示版本号如 29.4.3
```

## 2. 启动 Dify 容器

```bash
cd "d:\git depository\pokemon-agent-platform\dify\docker"
docker compose -f docker-compose.yaml -f docker-compose.override.yml -p dify up -d
```

等待约 30 秒，验证所有容器运行：
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```
✅ 应看到 13 个容器（含 pokemon-tools），关键容器为 healthy

## 3. 启动 Ollama

```bash
ollama serve
```

验证模型：
```bash
ollama list
```
✅ 应看到 deepseek-r1:8b（或已安装的其他模型）

## 4. 启动 Pokemon Tools API

```bash
python "d:\git depository\pokemon-agent-platform\plugins\pokemon-tools\main.py"
```

验证：
```bash
curl http://localhost:8100/health
# ✅ 返回 {"status":"ok"}
```

## 5. 打开 Dify 页面

浏览器访问 **http://localhost**

登录凭据（保存于数据库）：
- 邮箱：`3775060926@qq.com`
- 密码：`gwbzs666`

---

## 环境变量（已持久化，无需重复设置）

| 变量 | 值 | 用途 |
|------|----|------|
| `OLLAMA_MODELS` | `D:\OllamaModels` | Ollama 模型存储位置 |

## 端口汇总

| 端口 | 服务 | 访问地址 |
|------|------|---------|
| 80 | Dify Web | http://localhost |
| 5432 | PostgreSQL | (仅内部) |
| 8100 | Pokemon Tools API | http://localhost:8100 |
| 11434 | Ollama API | (仅内部) |

## 快速检查脚本

```bash
# 一键检查所有服务
echo === Docker === && docker info --format '{{.ServerVersion}}' && echo === Dify Containers === && docker ps --format '{{.Names}}' | findstr dify && echo === Ollama === && curl -s http://localhost:11434/api/tags | python -c "import sys,json;d=json.load(sys.stdin);print(f'{len(d.get(\"models\",[]))} models')" && echo === Pokemon Tools === && curl -s http://localhost:8100/health
```

## 关闭顺序

1. Ctrl+C 停 Pokemon Tools API
2. Ctrl+C 停 Ollama
3. `docker compose -p dify down` （或保留容器仅关闭 Docker Desktop）
