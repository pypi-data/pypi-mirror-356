import typer
from unieai_excel_temp_mcp.__main__ import app as excel_cli  # 引入原 server 启动器

def main():
    typer.run(excel_cli)

if __name__ == "__main__":
    main()
