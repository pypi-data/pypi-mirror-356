import shutil
from excel_mcp.tools import excel_write_to_sheet
import mcp
import logging
import unieai_excel_temp_mcp

logger = logging.getLogger(__name__)

@mcp.tool()
def write_data_to_excel_with_custom(
    filepath: str,
    outputpath: str,
    data: dict,
) -> str:
    """
    使用自訂的 fill_excel 函式將資料寫入 Excel 模板並儲存新檔案。

    參數:
      filepath (str): 原始 Excel 模板檔案路徑。
      outputpath (str): 填充後輸出的 Excel 檔案完整路徑。
      data (dict): 一個包含 key/value 的字典，用於替換模板中 {{key}} 的佔位符。

    回傳:
      str: fill_excel 回傳的訊息，通常為輸出檔案的完整路徑或錯誤訊息。

    範例:
      write_data_to_excel_with_custom(
          filepath="D:/excel_temp.xlsx",
          outputpath="D:/excel_filled.xlsx",
          data={"item": "產品A", "number": "2", "price": 10000}
      )
    """
    try:
        from unieai_excel_temp_mcp.fill_excel import fill_excel

        params = {
            "filepath": filepath,
            "outputpath": outputpath,
            "data": data
        }

        # 呼叫 fill_excel 將 data 填入模板並儲存為新檔
        result = fill_excel(params)
        return result

    except (ValidationError, DataError) as e:
        # 回傳明確的錯誤訊息
        return f"Error: {e}"
    except Exception as e:
        logger.error(f"Error writing data: {e}")
        # 若有未預期的錯誤，直接拋出供框架處理
        raise

