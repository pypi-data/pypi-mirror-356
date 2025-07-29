"""
mcp_lumerpy.mcp_server
~~~~~~~~~~~~~~~~~~~~~~
MCP wrapper that exposes *ANY* lumerpy top-level callable via a single
tool “call-func”.  Uses the official `mcp` async SDK, so Trae gets:
• 标准 initialize / initialized 握手      • listTools 自动函数说明
• JSON-Schema 参数校验                  • 富文本 / 文件返回能力
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any

import lumerpy

from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# -------------------------------------------------------------------
server = Server("mcp-lumerpy")   # MCP “宿主” 名称
# -------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Expose a single generic tool that can call any lumerpy function."""
    return [
        types.Tool(
            name="call-func",
            description=(
                "调用 lumerpy 顶层可调用对象\n\n"
                "参数说明:\n"
                "• method  : 函数名 (必填)\n"
                "• args    : 位置参数数组 (可选)\n"
                "• kwargs  : 关键字参数字典 (可选)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {"type": "string", "description": "lumerpy 顶层函数名"},
                    "args":   {"type": "array",  "items": {}, "default": []},
                    "kwargs": {"type": "object", "default": {}},
                },
                "required": ["method"],
            },
        )
    ]


@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict[str, Any] | None,
) -> list[types.TextContent]:
    """Handle execution of `call-func`."""
    if name != "call-func":
        raise ValueError(f"unknown tool {name}")

    if not arguments:
        raise ValueError("missing arguments")

    method = arguments["method"]
    args   = arguments.get("args", [])
    kwargs = arguments.get("kwargs", {})

    if not hasattr(lumerpy, method):
        raise ValueError(f"lumerpy has no attribute '{method}'")

    fn = getattr(lumerpy, method)
    if not callable(fn):
        raise ValueError(f"attribute '{method}' is not callable")

    # 参数校验：如果不匹配会抛 TypeError → 让用户改参数
    sig = inspect.signature(fn)
    sig.bind_partial(*args, **kwargs)  # 仅做匹配校验

    # 真正调用
    result = fn(*args, **kwargs)

    return [types.TextContent(type="text", text=str(result))]


# -------------------------------------------------------------------
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
# 其余 import 保持原样

# -----------------------------
async def async_main() -> None:
    async with stdio_server() as (reader, writer):
        await server.run(
            reader,
            writer,
            InitializationOptions(          # 👈 显式写初始化参数，版本跨 0.6 ~ 1.9 通用
                server_name="mcp-lumerpy",
                server_version="0.2.3",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main() -> None:                      # 同步入口供 uvx 调用
    import asyncio, sys
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":               # 允许 “python -m …” 直接运行
    main()
