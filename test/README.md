# 测试脚本索引

> 所有测试脚本都在此目录下。临时脚本放在 `temp/` 中，完成后需清理或归入正式测试文件。
> 需要测试时，先查此索引，有现成脚本直接使用，无需重复创建。

---

## 认证工具

| 文件 | 说明 | 用法 |
|------|------|------|
| `auth_login.py` | Dify 登录认证，获取 opener + csrf_token | `python auth_login.py` |

## Agent 测试

| 文件 | 说明 | 用法 |
|------|------|------|
| `test_agent_toolcall.py` | 测试 Agent 工具调用链路，流式输出关键事件 | `python test_agent_toolcall.py ["自定义查询"]` |
| `test_tool_api.py` | 直接测试 pokemon-tools API（绕过 Agent） | `python test_tool_api.py` |

## 模型管理

| 文件 | 说明 | 用法 |
|------|------|------|
| `db_model_manager.py` | 通过数据库管理 Dify 模型（添加/切换） | `python db_model_manager.py list` |
| | | `python db_model_manager.py add <模型名>` |
| | | `python db_model_manager.py switch <模型名>` |

## 提供商查询

| 文件 | 说明 | 用法 |
|------|------|------|
| `check_providers.py` | 查看 Dify 模型提供商及所需参数 | `python check_providers.py` |
| | | `python check_providers.py ollama`（过滤） |

## 临时脚本

临时测试脚本放在 `temp/` 目录下，使用后标记完成或整合到正式测试文件。

---

## 快速测试链路

```bash
# 1. 验证 pokemon-tools API
python test_tool_api.py

# 2. 验证 Agent 工具调用
python test_agent_toolcall.py "查询喷火龙的属性"

# 3. 查看当前 Dify Ollama 模型
python db_model_manager.py list
```
