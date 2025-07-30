# PKULAW MCP server for law search

A MCP server for law search presented by [PKULAW](https://www.pkulaw.com/).


## Functions

This MCP server provides functions to search law and regulations powered by [PKULAW](https://www.pkulaw.com/). This search is semantic search, leveraging embeddings.


## Use in MCP client

Use following conf to add to local MCP client:

```json
{
  "mcpServers": {
    "pkulaw-mcp-law-search": {
      "command": "uvx",
      "args": ["pkulaw-mcp-law-search"],
      "env": {
        "PKULAW_API_KEY": "your_pkulaw_api_key"
      }
    }
  }
}
```

For API key, please contact: <fxtj@chinalawinfo.com>.

In LLM chat, first enable this MCP server, and input like followings：
- 法律中关于危险货物的定义是什么？
- 请给出以下法规的内容：危险货物道路运输安全管理办法。

If the MCP client fail to invoke, you may need to explictly enable tool calling, like:
- 请使用工具回答，法律中关于危险货物的定义是什么？


