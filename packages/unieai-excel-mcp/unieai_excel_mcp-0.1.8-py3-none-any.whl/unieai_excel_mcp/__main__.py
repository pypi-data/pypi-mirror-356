# unieai_excel_mcp/__main__.py

import typer

def app():
    # 匯入 MCP tool，確保工具會被註冊
    from unieai_excel_mcp.tools import write_excel  # noqa: F401
    typer.echo("Tool 已註冊，可透過 `mcp run` 使用")

if __name__ == "__main__":
    typer.run(app)