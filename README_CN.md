# 社交平台内容自动生成与发布管理平台

本项目的宗旨是：让您一句话输入主题，便可以得到全平台的内容搜索和发布，并保证内容的质量、排版、多样性等。
争取早日支持：小红书、今日头条、抖音、youtube等平台的内容发布


## 本项目技术栈
### 后端
- python
- fastapi
- agentscope
- mcp
- aiohttp

### 前端
- **原生HTML/CSS/JavaScript** - 轻量级，无需构建
- **Element UI 风格** - 简洁美观的UI设计
- **响应式布局** - 支持桌面和移动端

### MCP工具服务
- **Jina MCP Tools** - 网络搜索和内容抓取
- **Tavily Remote** - 深度网络搜索
- **XHS MCP** - 小红书内容发布


## 项目架构介绍

```
social-media-management-agent/
├── app.py                      # FastAPI主程序
├── requirements.txt            # Python依赖
├── README_CH.md                # 本文档
├── main.py                     # 项目本地启动调试入口
|
├── configs/                     # 配置模块
│   ├── __init__.py
│   ├── config_manager.py       # 配置管理器
│   ├── app_config.json         # 应用配置（自动生成）
│   ├── servers_config.json     # MCP服务配置（自动生成）
│   └── .env                    # 环境变量（自动生成）
│
├── src/                       # 核心功能模块
│   ├── __init__.py
│   ├── agent/                  # 智能体模块
│   ├── tools/                  # 工具模块，包括mcp工具和普通工具
│   ├── memory/                 # 记忆模块，用于支持记忆保存和压缩，后续可扩展至历史会话记录，支持多轮对话策略
│
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css          # 样式文件
│   └── js/
│       └── app.js             # 前端交互逻辑
│
└── templates/                 # HTML模板
    └── index.html             # 主页面
```
### 自动生成的配置文件说明
#### 1. app_config.json

存储应用的主要配置信息：

```json
{
  "llm_api_key": "sk-xxx...",
  "openai_base_url": "https://api.openai.com/v1",
  "default_model": "claude-sonnet-4-20250514",
  "jina_api_key": "jina_xxx...",
  "tavily_api_key": "tvly_xxx...",
  "xhs_mcp_url": "http://localhost:18060/mcp"
}
```

#### 2. servers_config.json

MCP服务器配置（根据app_config.json自动生成）：

```json
{
  "mcpServers": {
    "jina-mcp-tools": {
      "command": "npx",
      "args": ["jina-mcp-tools"],
      "env": {
        "JINA_API_KEY": "jina_xxx..."
      }
    },
    "tavily-remote": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.tavily.com/mcp/?tavilyApiKey=tvly_xxx..."]
    },
    "xhs": {
      "type": "streamable_http",
      "url": "http://localhost:18060/mcp"
    }
  }
}
```

## 项目运行指南
### 1. 启动小红书MCP服务

**必须先启动 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 服务**


```bash
# 1. 克隆小红书MCP项目
git clone https://github.com/xpzouying/xiaohongshu-mcp.git
cd xiaohongshu-mcp

# 2. 按照项目README的说明启动服务
# 默认服务地址: http://localhost:18060/mcp
```
⚠️注意：要先登录自己的小红书账号（按照这个 mcp 服务里面的方式来进行登录）
### 2. 系统环境

- Python 3.8+
- Node.js 16+ (用于MCP工具)
- npm/npx (用于运行MCP工具)

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ./Social-Media-Management-Agent
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py
```

应用默认在 `http://localhost:8080` 启动。

### 3. 配置系统

访问 `http://localhost:8080`，在左侧面板配置以下信息：

#### 必填配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| **LLM API Key** | OpenAI兼容的API密钥 | `sk-xxx...` |
| **OpenAI Base URL** | API基础地址 | `https://api.openai.com/v1` 或 `https://usw.sealos.io/v1` |
| **默认模型** | 使用的LLM模型 | `claude-sonnet-4-20250514` (推荐) |
| **小红书MCP服务地址** | MCP服务的URL | `http://localhost:18060/mcp` |

#### 可选配置

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| **Jina API Key** | Jina搜索服务密钥 | [Jina官网](https://jina.ai/) |
| **Tavily API Key** | Tavily搜索服务密钥 | [Tavily官网](https://tavily.com/) |

推荐使用 Tavily 作为搜索工具，每个月能白嫖 1000 次搜索请求

> 💡 **提示**: 点击配置项旁边的"获取密钥"或"查看文档"链接可直接跳转到对应的服务网站。


### 4. 生成内容

1. 在"内容生成与发布"区域输入主题
2. 点击"🚀 开始生成并发布"按钮
3. 在右侧查看执行进度和最终结果


## ROADMAP 未来计划
### 完善功能
- [ ] 增加对其他社交媒体平台的支持
- [ ] 完善记忆模块，支持多轮对话
- [ ] 增加内容分析和优化功能，支持自主调整提示词，自主管理工具和记忆
- [ ] 历史会话展示和回顾
- [ ] 优化前端用户界面

### 支持的平台
- [x] 小红书 (Xiaohongshu) - 已支持内容搜索和发布
- [ ] 今日头条 - 计划中
- [ ] youtube - 计划中
- [ ] 抖音 (TikTok) - 计划中
- [ ] 快手 (Kuaishou) - 计划中


## 📝 许可证

本项目仅供学习和研究使用。使用本项目时请遵守：
- OpenAI API使用条款
- 小红书平台规则
- 各MCP服务提供商的使用协议


## 注意注意

本项目还处于较为早期阶段，目前功能性还不够完善，可以作为agentscope 构建agent项目学习使用，避免在生产环境中使用。


## 参考项目
1、[xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
2、xiaohongshu 项目的页面（git链接遗忘，忘见谅）
3、agentscope