import re
from pathlib import Path
from typing import List

def parse_repo_name(github_url: str) -> str:
    """从GitHub URL中解析仓库名称。"""
    match = re.search(r"/([^/]+?)(?:\.git)?$", github_url)
    if not match:
        raise ValueError(f"无法从URL '{github_url}' 中解析仓库名称。")
    return match.group(1)

def create_project_folders(repo_name: str, base_dir: Path) -> List[Path]:
    """
    在指定的基础目录下为仓库创建标准项目文件夹。
    :param repo_name: 仓库名称。
    :param base_dir: 用于创建项目文件夹的基础目录。
    :return: 一个包含所有被创建文件夹路径的列表。
    """
    project_path = base_dir / repo_name
    subfolders = ["Input", "Output", "Logs", "Config"]
    created_paths: List[Path] = []
    project_path.mkdir(parents=True, exist_ok=True)
    created_paths.append(project_path)
    for folder in subfolders:
        subfolder_path = project_path / folder
        subfolder_path.mkdir(exist_ok=True)
        created_paths.append(subfolder_path)
    return created_paths 