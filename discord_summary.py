#!/usr/bin/env python3
"""
Discord 聊天记录翻译+总结工具

使用方法:
  python discord_summary.py

需要设置环境变量:
  export ANTHROPIC_API_KEY=你的Claude_API_Key
  export DISCORD_TOKEN=你的Discord_Token
"""

import os
import sys
import requests
import anthropic
from datetime import datetime, timezone


DISCORD_API = "https://discord.com/api/v10"


def get_headers(token):
    return {"Authorization": token}


def get_channels(guild_id, token):
    """获取服务器所有频道"""
    resp = requests.get(f"{DISCORD_API}/guilds/{guild_id}/channels", headers=get_headers(token))
    if resp.status_code == 401:
        print("错误：Discord Token 无效，请重新获取")
        sys.exit(1)
    if resp.status_code == 403:
        print("错误：没有权限访问这个服务器")
        sys.exit(1)
    resp.raise_for_status()
    channels = resp.json()
    # 只返回文字频道（type=0）
    return [c for c in channels if c.get("type") == 0]


def get_messages(channel_id, token, limit=200):
    """获取频道最近消息"""
    messages = []
    last_id = None

    while len(messages) < limit:
        batch_size = min(100, limit - len(messages))
        params = {"limit": batch_size}
        if last_id:
            params["before"] = last_id

        resp = requests.get(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=get_headers(token),
            params=params
        )
        if resp.status_code == 403:
            return None  # 没有权限读这个频道
        resp.raise_for_status()

        batch = resp.json()
        if not batch:
            break

        messages.extend(batch)
        last_id = batch[-1]["id"]

        if len(batch) < batch_size:
            break

    # 按时间正序排列
    return list(reversed(messages))


def format_messages(messages):
    lines = []
    for msg in messages:
        timestamp = msg.get("timestamp", "")[:10]
        author = msg.get("author", {}).get("username", "未知")
        content = msg.get("content", "").strip()
        if content and len(content) > 1:
            lines.append(f"[{timestamp}] {author}: {content}")
    return "\n".join(lines)


def summarize(messages_text, channel_name, guild_name):
    client = anthropic.Anthropic()

    prompt = f"""你是一个帮助中文用户理解英文 Discord 聊天记录的助手。

以下是 Discord 服务器「{guild_name}」的「#{channel_name}」频道最近的聊天记录：

---
{messages_text}
---

请用中文完成以下任务（像给朋友发消息一样自然，不需要太正式）：

**重点信息**（3-8条）
列出最重要的公告、机会、截止日期等（如招聘、活动、申请链接）

**活跃话题**（3-5条）
总结大家在讨论什么，哪个话题最热

**实用资源**
有没有链接、工具、或特别有价值的内容？没有就写"本期无"

**整体氛围**
用1-2句话描述这个频道最近的状态

注意：英文缩写或网络用语（如OA、LC、referral、SWE、intern、FAANG等）请在括号里加中文解释。"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def main():
    # 检查环境变量
    token = os.environ.get("DISCORD_TOKEN")
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not token:
        print("错误：请先设置 Discord Token")
        print("运行: export DISCORD_TOKEN=你的Token")
        sys.exit(1)

    if not api_key:
        print("错误：请先设置 Anthropic API Key")
        print("运行: export ANTHROPIC_API_KEY=你的APIKey")
        sys.exit(1)

    # 输入服务器 ID
    guild_id = input("请输入服务器 ID（直接回车使用默认 861966823054639134）: ").strip()
    if not guild_id:
        guild_id = "861966823054639134"

    print(f"\n正在获取频道列表...")
    channels = get_channels(guild_id, token)

    if not channels:
        print("没有找到任何文字频道")
        sys.exit(0)

    # 显示频道列表
    print(f"\n找到 {len(channels)} 个频道：")
    for i, ch in enumerate(channels):
        print(f"  {i+1}. #{ch['name']}")

    # 选择频道
    print("\n请选择要总结的频道（输入编号，多个用逗号分隔，直接回车选前5个）: ", end="")
    choice = input().strip()

    if not choice:
        selected = channels[:5]
    else:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        selected = [channels[i] for i in indices if 0 <= i < len(channels)]

    # 获取服务器名称
    resp = requests.get(f"{DISCORD_API}/guilds/{guild_id}", headers=get_headers(token))
    guild_name = resp.json().get("name", "未知服务器") if resp.ok else "未知服务器"

    # 逐个频道总结
    for ch in selected:
        print(f"\n正在读取 #{ch['name']} 的消息...")
        messages = get_messages(ch["id"], token, limit=200)

        if messages is None:
            print(f"  跳过（没有权限读取此频道）")
            continue

        if not messages:
            print(f"  跳过（频道内没有消息）")
            continue

        date_start = messages[0].get("timestamp", "")[:10]
        date_end = messages[-1].get("timestamp", "")[:10]
        print(f"  获取到 {len(messages)} 条消息（{date_start} 至 {date_end}）")
        print(f"  正在生成中文摘要...")

        messages_text = format_messages(messages)
        summary = summarize(messages_text, ch["name"], guild_name)

        line = "=" * 55
        print(f"\n{line}")
        print(f"  {guild_name}  /  #{ch['name']}")
        print(f"  {date_start} 至 {date_end}  （共 {len(messages)} 条消息）")
        print(line)
        print()
        print(summary)
        print()

    print("=" * 55)
    print(f"完成！生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
