import os
from pathlib import Path
from typing_extensions import Annotated
import typer
from rich.console import Console
from gbk_diy_github_files.core import create_project_folders, parse_repo_name

app = typer.Typer(
    help="通过GitHub仓库URL，快速创建标准项目文件夹结构。",
    add_completion=False,
)
console = Console()
DEFAULT_BASE_DIR = os.environ.get("DIY_GF_HOME", r"D:\\github")

@app.command()
def create(
    github_url: Annotated[
        str,
        typer.Argument(
            help="GitHub仓库的完整HTTPS URL。",
            show_default=False,
        ),
    ],
    directory: Annotated[
        Path,
        typer.Option(
            "--directory",
            "-d",
            help=f"指定项目创建的基础目录。如果未提供，默认为: {DEFAULT_BASE_DIR}",
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ] = Path(DEFAULT_BASE_DIR),
):
    """
    解析GitHub URL并创建项目文件夹。
    """
    try:
        with console.status("[bold yellow]正在处理...[/bold yellow]", spinner="dots"):
            repo_name = parse_repo_name(github_url)
            console.log(f"解析到仓库名称: [cyan]{repo_name}[/cyan]")
            created_paths = create_project_folders(repo_name, directory)
            console.log(f"目标基础目录: [cyan]{directory}[/cyan]")
        console.print("\n[bold green]🎉 项目文件夹创建成功！[/bold green]")
        for path in created_paths:
            if path.name == repo_name:
                console.print(f"主目录: [bold yellow]{path}[/bold yellow]")
            else:
                console.print(f"  子目录: [green]{path}[/green]")
    except ValueError as e:
        console.print(f"[bold red]错误: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]发生未知错误: {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 