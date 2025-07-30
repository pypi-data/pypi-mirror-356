# gbk-diy-github-files

一个通过GitHub仓库URL，快速创建标准项目文件夹结构的CLI工具。

## 功能

- 解析任何GitHub仓库URL（支持 `https://.../repo` 和 `https://.../repo.git` 格式）。
- 在指定目录（默认为 `D:\github`）下创建以仓库名命名的主文件夹。
- 在主文件夹内自动创建 `Input`, `Output`, `Logs`, `Config` 四个标准子文件夹。

## 安装

```bash
pip install gbk-diy-github-files
```

## 使用方法

### 基本用法

这将在默认位置 (D:\github) 创建一个 faster-whisper 文件夹和其子文件夹。

```bash
diy-gf create https://github.com/SYSTRAN/faster-whisper.git
```

### 指定目录

这将在 E:\my_projects 目录下创建 my-cool-project 文件夹。

```bash
diy-gf create https://github.com/user/my-cool-project -d E:\my_projects
```

或者使用短选项：

```bash
diy-gf create https://github.com/user/my-cool-project -d E:\my_projects
```

### 帮助信息

```bash
diy-gf --help
diy-gf create --help
``` 