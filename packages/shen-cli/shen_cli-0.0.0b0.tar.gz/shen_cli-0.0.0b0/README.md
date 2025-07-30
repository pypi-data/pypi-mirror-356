# Shen

[![PyPI version](https://badge.fury.io/py/shen-cli.svg)](https://badge.fury.io/py/shen-cli)
[![Python Version](https://img.shields.io/pypi/pyversions/shen-cli.svg)](https://pypi.org/project/shen-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这个项目会是一个AI命令行工具，专注于处理编程以外的事情

因为我看到了Claude Code神一样的编程能力，他的交互和效果令我惊讶。

因此我在寻找一个类似的命令行工具，这个命令行工具不是专注于编程的，而是专注于处理其他工作。
让使用者能得到更大的效率提升。

这是一个探索性的项目，主要是为了探索CLI+MCP结合帮助使用者完成工作的常规任务。

选择使用python实现

## FAQ
### 为什么是做命令行工具？

1. 目前已经很多通用GUI的AI软件、AI IDE、AI plugin了，所以再做一个轮子的意义感觉不大
2. 如果你使用AI的强度比较高，你一定感受到了，无论是cursor还是augment之类的AI IDE或者是vscode插件，都受到其本身的制约，无法发挥出最强能力，这种情况无法避免，而Claude Code是CLI，因此他避开了这个问题。
3. 不一定所有的工作都在前台完成，也不一定所有的工作都在个人计算机完成。CLI会带来更多玩法和可能性，也许能派遣他到服务器上去（得足够安全），或者在后台运行，自动化通过TODOs读取任务并解决

### CLI的优势是什么？

1. CLI有更强的跨平台性（虽然普通用户可能会无法使用）
2. CLI受到的限制更少，能拥有的操作权限更大
3. 更多任务的并行可能
4. 更强的集成能力，他应该能被其他软件集成，就像ffmpeg那样


### 可能的工作？

他可能会聚合很多MCP服务，理解整个计算机中有哪些文档和软件，帮助用户完成文档整理、垃圾清理、提供必要信息、制作excel、world、安全检查、软件安装（软件安装我觉得对我一直很头疼，总是报错很烦）等一些常规工作

---

不过目前的确没有想好他和Claude Code的真正差异是什么，感觉Claude Code除了写代码，其他事情也干的不错。
我还得仔细思考一下。

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install shen-cli
```

### 从源码安装

```bash
git clone https://github.com/shenjingnan/shen.git
cd shen
pip install -e .
```

## 使用方法

### 基本命令

```bash
# 查看版本
shen --version

# 查看帮助
shen --help

# 获取 Shen 信息
shen info

# 列出可用插件
shen plugins

# 运行任务
shen run "帮我整理下载文件夹"

# 交互模式运行任务
shen run "检查系统安全" --interactive
```

### 调试模式

```bash
# 启用调试模式
shen --debug info
```

## 开发

### 环境设置

```bash
# 安装 Poetry
pip install poetry

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行测试并查看覆盖率
poetry run pytest --cov

# 运行特定测试
poetry run pytest tests/test_cli.py
```

### 代码质量

```bash
# 格式化代码
poetry run black src tests

# 代码检查
poetry run ruff check src tests

# 类型检查
poetry run mypy src

# 运行所有检查
poetry run black src tests && poetry run ruff check src tests && poetry run mypy src
```

### 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
