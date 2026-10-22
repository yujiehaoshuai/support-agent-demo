# 小店售后 Agent（个人学习项目）

Python + LangChain/LangGraph + Streamlit + SQLite。基于开源聊天模板结构改造，提供政策检索、订单查询、人工确认工单、会话记忆和工具调用记录。适合 Python 后端 / AI 应用开发面试。

## 启动

在本目录 PowerShell 执行：

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py --server.address 127.0.0.1
```

或运行 start.ps1。新环境先 `python -m venv .venv`，再 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`。

默认离线模式无需密钥，只演示工具和业务流程，不是大模型推理。真实模型模式需要先设置 OPENAI_API_KEY，可选 OPENAI_BASE_URL、OPENAI_MODEL，再启动程序。不要将密钥写入仓库。

## 5分钟演示

1. 输入“A1001退货运费谁承担”，观察订单和带来源政策。
2. 输入“A1002”，演示后端拒绝访问其他账户订单。
3. 输入“发票”，展示知识覆盖不足。
4. 展开工单区，输入 A1001 和退货原因，确认后提交。
5. 重复提交相同内容，工单编号不变。
6. 配置模型后切换真实模式，观察模型选择工具与调用记录。

## 设计与边界

- owner 固定在服务端，模型工具签名不接受 owner；这只是权限隔离演示，没有实现登录系统。
- SQLite 参数化查询避免拼接 SQL；唯一约束实现同订单同原因的提交幂等。
- 写操作不暴露给模型，通过表单明确确认。只是登记工单，不会退款。
- 使用 LangGraph 内存检查点保存当前会话；清空或重启后丢失。工单持久化到 SQLite。
- 政策为3条中文关键词规则，尚非向量 RAG；同义词召回有限。
- 模型调用超时30秒、重试1次、图执行步数上限12。没有宣称生产级可用性。

## 面试与简历

建议表述：基于开源 LangGraph 聊天模板二次开发售后助手，封装订单查询与政策检索工具，使用 SQLite 实现工单持久化与幂等提交；通过服务端账户约束、人工确认写入和工具执行记录提高流程可控性，并编写权限隔离、重复提交及未知知识场景测试。

不要写不存在的用户规模、准确率提升或线上部署经历。应能解释：为什么权限不能只靠提示词、唯一约束如何处理重复提交、为什么模型不直接退款、关键词检索如何升级为混合检索、内存检查点和数据库持久化的区别。

## 网上筛选的候选

| 项目 | 适合方向 | 取舍 |
|---|---|---|
| https://github.com/hwchase17/langchain-streamlit-template | 工具调用聊天助手 | 本次采用，结构小便于理解 |
| https://github.com/langchain-ai/streamlit-agent | 搜索 / 数据分析 Agent 示例 | 项目已归档，旧依赖和代码执行工具需要额外审查 |
| https://github.com/microsoft/autogen/tree/main/python/samples/agentchat_fastapi | FastAPI Agent 服务 | 适合后续补接口，不必从多智能体大系统开始 |

## 来源记录

2026-10-22 参考 https://github.com/hwchase17/langchain-streamlit-template 。原始快照仅保留在开发机器，未包含在本仓库。

main.py 参考模板的 Streamlit + Agent 会话思路，重新实现业务界面；support.py 和测试为新增。上游快照未附 LICENSE，因此未将其源码随仓库分发。本项目明确保留设计来源说明。

测试命令：`python -m unittest -v test_support.py`。真实模型端到端验证需要有效 API 配置。

## 本机验证结果（2026-10-22）

Windows / Python 3.14.5，依赖版本已锁定在 requirements.txt。

- 业务测试6项全部通过，包括越权、SQL注入输入、幂等和未知政策。
- `smoke_ui.py` 通过：实际 Streamlit 页面渲染、聊天输入和确认建单交互。
- `smoke_agent.py` 通过：真实 ChatOpenAI 适配器和 Agent 图构建（不请求模型）。
- Streamlit 服务成功监听 127.0.0.1:8501。
- 未提供真实 API 密钥，尚未验证模型回答质量、工具选择准确率和外部接口可用性。
