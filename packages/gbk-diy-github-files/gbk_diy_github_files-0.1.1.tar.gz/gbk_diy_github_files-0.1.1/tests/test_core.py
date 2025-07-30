import pytest
from pathlib import Path
from gbk_diy_github_files.core import parse_repo_name, create_project_folders

def test_parse_repo_name_with_git_suffix():
    url = "https://github.com/SYSTRAN/faster-whisper.git"
    assert parse_repo_name(url) == "faster-whisper"

def test_parse_repo_name_without_git_suffix():
    url = "https://github.com/wanderer-gbk/gbk-diy-github-files"
    assert parse_repo_name(url) == "gbk-diy-github-files"

def test_parse_repo_name_invalid_url():
    with pytest.raises(ValueError):
        parse_repo_name("not a valid url")

def test_create_project_folders(monkeypatch):
    mock_mkdir_calls = []
    def mock_mkdir(self, parents=False, exist_ok=False):
        mock_mkdir_calls.append(self)
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    repo_name = "my-test-repo"
    base_dir = Path("/fake/dir")
    create_project_folders(repo_name, base_dir)
    expected_paths = [
        base_dir / repo_name,
        base_dir / repo_name / "Input",
        base_dir / repo_name / "Output",
        base_dir / repo_name / "Logs",
        base_dir / repo_name / "Config",
    ]
    assert len(mock_mkdir_calls) == len(expected_paths)
    assert set(map(str, mock_mkdir_calls)) == set(map(str, expected_paths)) 