# Discord 中文摘要工具 | Discord Chinese Summary Tool

[中文](#中文) | [English](#english)

---

## 中文

一个帮助中文用户快速理解英文 Discord 社群动态的工具。

自动读取 Discord 频道消息，调用 Claude AI 翻译并生成中文摘要，让你不用花时间看密集的英文聊天记录也能掌握重点。

### 背景

加入了一些英文 Discord 社群（如找工2026SWE、Google Gemini Hackathon），但面临三个问题：
1. 消息太多，根本看不过来
2. 英文不流利，网络用语更难懂
3. 没有时间逐条阅读

所以做了这个工具。

### 效果示例

```
=======================================================
  找工2026SWE  /  #job-postings
  2026-02-20 至 2026-02-27  （共 200 条消息）
=======================================================

**重点信息**
- Google 2026 SWE 暑期实习（Summer Internship）开放申请，截止 3/15
- 有人分享了微软内推（Referral）链接，见2月25日消息
- Leetcode（力扣）OA（Online Assessment 在线笔试）主要考图和动态规划

**活跃话题**
- 简历格式讨论（热度最高，约80条）
- 面试经验分享（约50条）
- 各公司HC（Headcount 招聘名额）是否缩减

**实用资源**
- 有人整理了2026 SWE 开放申请公司列表（谷歌文档链接）

**整体氛围**
求职季焦虑感明显，大家都在互相分享信息和鼓励。
```

### 使用前提

- Python 3.x
- [Anthropic API Key](https://console.anthropic.com)（需要充值，处理一次约 $0.01）
- Discord 账号的 Token（从浏览器开发者工具获取）

### 安装

```bash
# 创建虚拟环境
python3 -m venv discord-env
source discord-env/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 使用方法

```bash
# 设置环境变量
export DISCORD_TOKEN=你的Discord_Token
export ANTHROPIC_API_KEY=你的Claude_API_Key

# 运行
python discord_summary.py
```

运行后：
1. 输入服务器 ID（在 Discord 右键服务器图标 → 复制服务器 ID）
2. 从频道列表中选择想要总结的频道
3. 等待生成，获得中文摘要

### 如何获取 Discord Token

1. 浏览器打开 [discord.com/app](https://discord.com/app)
2. 按 `Command + Option + I` 打开开发者工具
3. 点击 **Network（网络）** 标签
4. 在 Discord 里点任意频道
5. 找任意一条 API 请求 → Request Headers → `authorization` 字段
6. 复制该值（即为 Token）

> ⚠️ Token 相当于账号密码，不要泄露给任何人

### 技术栈

- Python 3
- [Anthropic Claude API](https://anthropic.com) — 翻译和摘要
- Discord REST API — 读取消息

### 学习历程

这是我作为编程新手独立完成的第一批项目之一，记录一下踩过的坑：

| 遇到的问题 | 原因 | 解决方法 |
|-----------|------|---------|
| `pip: command not found` | Mac 默认没有 pip | 改用 `pip3` |
| pip3 报 externally-managed 错误 | macOS 系统保护机制 | 创建虚拟环境（venv） |
| DiscordChatExporter 被 Mac 删除 | Gatekeeper 安全机制拦截未签名程序 | 放弃第三方工具，改用 Python 直接调 Discord API |
| Console 粘贴代码被 Discord 拦截 | Discord 反诈提示 | 改用 Network 标签观察请求头获取 Token |
| `ModuleNotFoundError: requests` | 依赖未安装 | `pip install requests` |
| API 余额不足 | 新账号需要手动充值 | 在 console.anthropic.com 充值 |

---

## English

A tool that helps Chinese-speaking users quickly understand what's happening in English Discord communities.

It reads Discord channel messages via API and uses Claude AI to generate concise Chinese summaries — so you can stay up to date without reading through hundreds of English messages.

### Background

I joined several English Discord servers (e.g. 找工2026SWE for SWE job hunting, Google Gemini Hackathon) but faced three problems:
1. Too many messages to keep up with
2. English is hard to read, especially internet slang
3. Not enough time to read everything

So I built this tool.

### Prerequisites

- Python 3.x
- [Anthropic API Key](https://console.anthropic.com) (costs ~$0.01 per run)
- Your Discord user Token (retrieved from browser DevTools)

### Installation

```bash
# Create a virtual environment
python3 -m venv discord-env
source discord-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Set environment variables
export DISCORD_TOKEN=your_discord_token
export ANTHROPIC_API_KEY=your_claude_api_key

# Run
python discord_summary.py
```

After running:
1. Enter the server ID (right-click the server icon in Discord → Copy Server ID)
2. Select which channels to summarize from the list
3. Wait a few seconds and receive your Chinese summary

### How to Get Your Discord Token

1. Open [discord.com/app](https://discord.com/app) in Chrome
2. Press `Command + Option + I` to open DevTools
3. Click the **Network** tab
4. Click any channel in Discord
5. Find any API request → Request Headers → `authorization` field
6. Copy that value — that's your Token

> ⚠️ Your Token is equivalent to your password. Never share it with anyone.

### Tech Stack

- Python 3
- [Anthropic Claude API](https://anthropic.com) — translation and summarization
- Discord REST API — fetching messages

### Project Structure

```
discord-chinese-summary/
├── discord_summary.py   # main script
├── requirements.txt     # dependencies
└── README.md
```

### Lessons Learned

This is one of my first projects as a beginner coder. Here are the obstacles I ran into:

| Problem | Cause | Solution |
|---------|-------|----------|
| `pip: command not found` | pip not available by default on Mac | Use `pip3` instead |
| `pip3` externally-managed error | macOS system protection | Create a virtual environment (venv) |
| DiscordChatExporter deleted by Mac | Gatekeeper blocked unsigned binary | Dropped the tool, used Discord API directly in Python |
| Console paste blocked by Discord | Discord's anti-scam warning | Used Network tab to find Token in request headers instead |
| `ModuleNotFoundError: requests` | Missing dependency | `pip install requests` |
| API credit balance too low | New accounts need manual top-up | Added credits at console.anthropic.com |

---

*Built with assistance from Claude Code*
