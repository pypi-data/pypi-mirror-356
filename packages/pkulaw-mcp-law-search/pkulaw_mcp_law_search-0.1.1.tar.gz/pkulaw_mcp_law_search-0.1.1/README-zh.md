# 北大法宝法律智能检索MCP服务

这是[北大法宝](https://www.pkulaw.com/)提供的用于法律法规智能检索的MCP服务。

北大法宝——让法律更智能。


## 功能

此MCP服务提供了法律法规智能检索功能。使用文本嵌入，进行语义检索。


## MCP客户端使用

在MCP客户端（比如CherryStudio）里，使用以下配置安装运行此MCP服务:

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

申请试用API key，请联系: <fxtj@chinalawinfo.com>.

在大模型对话的工具栏，首先启用此MCP服务，然后输入类似以下的内容，调用MCP服务完成回答：
- 法律中关于危险货物的定义是什么？
- 请给出以下法规的内容：危险货物道路运输安全管理办法。

如果MCP客户端没有调用MCP服务，在输入开头加入“请使用工具回答”进行提示：
- 请使用工具回答，法律中关于危险货物的定义是什么？


