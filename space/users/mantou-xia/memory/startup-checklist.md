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

## 2. Dify 容器（自动启动）

Dify 容器已配置 restart: unless-stopped，**随 Docker Desktop 自动启动**，无需手动执行 `docker compose up`。

首次部署或清理后需执行：
```bash
cd "d:\git depository\pokemon-agent-platform\dify\docker"
docker compose -p dify up -d
```

验证：
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
# ✅ 关键容器状态为 healthy (api, db_postgres, sandbox)
```

> ⚠️ 注意：如果看到两套容器（`dify-*` 和 `docker-*`），说明有重复 compose project。
> 保留 `docker-*` 项目（带 nginx:80），停掉 `docker compose -p dify down`。

## 3. 修复 nginx 502 错误（如遇 API 502）

如果 `http://localhost/console/api/login` 返回 502 Bad Gateway，
是 nginx 缓存了旧的 API 容器 IP。重启即可：
```bash
docker restart docker-nginx-1
```

## 4. 启动 Pokemon Tools API

```bash
python "d:\git depository\pokemon-agent-platform\plugins\pokemon-tools\main.py"
```

验证：
```bash
curl http://localhost:8100/health
# ✅ 返回 {"status":"ok"}
```

## 5. 启动 Ollama

```bash
ollama serve
```

验证模型：
```bash
ollama list
# ✅ 应看到 deepseek-r1:8b（或已安装的其他模型）
```

> ⚠️ 注意：deepseek-r1:8b 约 4.9GB，需要约 8GB 可用 RAM 来加载。
> 如遇 "llama runner process has terminated" 错误，请检查：
> - C 盘可用空间（模型文件存储位置）
> - 系统可用内存
> - 可考虑使用更小的模型如 qwen2:1.5b

## 6. 打开 Dify 页面

浏览器访问 **http://localhost**

登录凭据（保存于数据库）：
- 邮箱：`3775060926@qq.com`
- 密码：`gwbzs666`

> 技术细节：Dify 的登录密码字段使用 **Base64 编码** 而非 RSA 加密。
> 编码示例：`gwbzs666` → `Z3dienM2NjY=`

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
echo === Docker === && docker info --format '{{.ServerVersion}}' && echo === Dify Containers === && docker ps --format '{{.Names}}' | findstr docker- && echo === Ollama === && curl -s http://localhost:11434/api/tags | python -c "import sys,json;d=json.load(sys.stdin);print(f'{len(d.get(\"models\",[]))} models')" && echo === Pokemon Tools === && curl -s http://localhost:8100/health
```

## 关闭顺序

1. Ctrl+C 停 Pokemon Tools API
2. Ctrl+C 停 Ollama
3. 直接关闭 Docker Desktop（容器保留 restart 策略下次自动启动）
