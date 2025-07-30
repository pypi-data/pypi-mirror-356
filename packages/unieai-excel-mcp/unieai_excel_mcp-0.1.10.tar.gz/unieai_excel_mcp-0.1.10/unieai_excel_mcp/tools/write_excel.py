from fastmcp import FastMCP
from unieai_excel_mcp.services.fill_excel import fill_excel

mcp = FastMCP("unieai-excel-mcp")

@mcp.tool()
def write_data_to_excel_with_custom(
    filepath: str,
    outputpath: str,
    data: dict,
) -> str:
    """
    將資料寫入 Excel 模板中對應的 {{key}} 位置。
    """
    try:
        return fill_excel({
            "filepath": filepath,
            "outputpath": outputpath,
            "data": data
        })
    except Exception as e:
        return f"Error: {e}"
