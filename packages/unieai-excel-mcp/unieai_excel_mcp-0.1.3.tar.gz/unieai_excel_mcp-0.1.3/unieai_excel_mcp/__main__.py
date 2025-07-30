import typer
from mcp import serve

def app():
    from unieai_excel_mcp.tools import write_excel  # 註冊 tool
    serve()

if __name__ == "__main__":
    typer.run(app)
