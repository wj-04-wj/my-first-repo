以下是完整的 uv 包管理工具使用教程：

------

# uv 包管理工具教程

> **uv** 是由 [Astral](https://astral.sh/) 团队（Ruff 的作者）使用 Rust 编写的极速 Python 包和项目管理工具。
> 它可以替代 `pip`、`virtualenv`、`pip-tools`、`pipx`、`poetry`、`pyenv` 等工具，速度比 pip 快 **10~100 倍**。

------

## 目录

1. [安装与配置](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#1-安装与配置)
2. [Python 版本管理](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#2-python-版本管理)
3. [项目初始化](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#3-项目初始化)
4. [依赖管理](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#4-依赖管理)
5. [环境同步与锁文件](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#5-环境同步与锁文件)
6. [运行与任务](https://www.qianwen.com/chat/22a43e6d032540059d285efd6804eed8?ch=tongyi_redirect#6-运行与任务)

------

## 1. 安装与配置

### 1.1 安装 uv

**macOS / Linux：**

```bash
# 使用 curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

**Windows：**

```powershell
# PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 winget
winget install --id=astral-sh.uv -e
```

**macOS（Homebrew）*：**

```bash
brew install uv
```

**通过 pip 安装*：**

```bash
pip install uv
```

安装后验证：

```bash
uv --version
# uv 0.x.x
```

### 1.2 升级 uv

```bash
# 独立安装器 — 使用内置自更新命令
uv self update

# 指定版本
uv self update 0.7.0

# Homebrew 用户
brew upgrade uv

# pip 用户
pip install --upgrade uv
```

### 1.3 Shell 补全

uv 支持 Bash / Zsh / Fish / Elvish / PowerShell 的命令补全。

**Bash：**

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
source ~/.bashrc
```

**Zsh*：**

```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Fish*：**

```bash
echo 'uv generate-shell-completion fish | source' >> ~/.config/fish/config.fish
echo 'uvx --generate-shell-completion fish | source' >> ~/.config/fish/config.fish
```

**PowerShell：**

```powershell
# 添加到 $PROFILE
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
Add-Content -Path $PROFILE -Value '(& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

### 1.4 IDE 集成

**VS Code：**

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）
2. 输入 `Python: Select Interpreter`
3. 选择项目下 `.venv/bin/python`（uv 自动创建的虚拟环境）

VS Code 通常能自动检测到 `.venv` 目录。若未自动识别，可在 `.vscode/settings.json` 中手动指定：

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

**PyCharm：**

1. `File` → `Settings` → `Project: <项目名>` → `Python Interpreter`
2. 点击齿轮图标 → `Add Interpreter` → `Existing`
3. 选择项目目录下的 `.venv/bin/python`

------

## 2. Python 版本管理

uv 内置了 Python 版本管理能力（替代 `pyenv`），可以直接下载安装和管理多个 Python 版本。

### 2.1 安装 Python 版本

```bash
# 安装指定版本
uv python install 3.12

# 安装精确小版本
uv python install 3.11.9

# 安装多个版本
uv python install 3.10 3.11 3.12 3.13

# 安装所有支持的版本（谨慎使用）
uv python install --all
```

### 2.2 查看可用 / 已安装的版本

```bash
# 列出所有可用的 Python 版本
uv python list

# 仅显示已安装的版本
uv python list --only-installed
```

### 2.3 固定项目 Python 版本（pin）

```bash
# 将当前项目的 Python 版本固定为 3.12
uv python pin 3.12
```

此命令会在项目根目录创建一个 **`.python-version`** 文件，内容为：

```
3.12
```

当你在该项目目录下运行 `uv run`、`uv sync` 等命令时，uv 会自动使用 `.python-version` 中指定的 Python 版本。

### 2.4 卸载 Python 版本

```bash
uv python uninstall 3.10
```

### 2.5 查找 Python 路径

```bash
# 查看 uv 管理的 Python 路径
uv python find

# 查找特定版本
uv python find 3.12
```

------

## 3. 项目初始化

### 3.1 新建项目

```bash
# 创建一个默认的应用（Application）项目
uv init my-project
cd my-project
```

生成的目录结构：

```
my-project/
├── pyproject.toml      # 项目元数据与依赖声明
├── README.md
├── .python-version     # 固定的 Python 版本
└── main.py            # 示例入口文件
```

`pyproject.toml` 示例：

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

### 3.2 项目模板

`uv init` 支持多种项目类型：

```bash
# 创建一个应用项目（默认）
uv init my-app

# 显式指定为应用项目
uv init --app my-app

# 创建一个库（Library）项目 — 用于发布到 PyPI
uv init --lib my-library

# 创建一个带 bare 结构的项目（仅生成 pyproject.toml）
uv init --bare my-project
```

**库项目与App项目的区别：**

| 特性               | `--app` (应用)   | `--lib` (库)     |
| ------------------ | ---------------- | ---------------- |
| 用途               | 可运行的应用程序 | 发布到 PyPI 的包 |
| 生成 `src/` 目录   | ❌                | ✅                |
| 包含 `py.typed`    | ❌                | ✅                |
| 包含 `__init__.py` | ❌                | ✅                |

### 3.3 从已有项目迁移

#### 从 `requirements.txt` 迁移

> pip freeze > requirements.txt

```bash
# 1. 在已有项目中初始化 uv 项目
cd existing-project
uv init --bare           # 仅创建 pyproject.toml，不覆盖已有文件

# 2. 导入 requirements.txt 中的依赖
uv add -r requirements.txt

# 3. 生成锁文件并安装
uv sync
```

#### 从 Poetry 迁移*

```bash
# uv 原生支持 pyproject.toml，可直接使用 Poetry 的项目文件
cd poetry-project

# 如果已有 pyproject.toml，直接同步即可
uv sync

# uv 会自动解析 [tool.poetry.dependencies] 中的依赖（兼容 Poetry 格式）
# 也可以手动将 [tool.poetry.dependencies] 改为 [project] 标准格式
```

#### 从 Pipenv 迁移*

```bash
cd pipenv-project

# 1. 导出 Pipfile.lock 中的依赖
pipenv requirements > requirements.txt

# 2. 初始化 uv 并导入
uv init --bare
uv add -r requirements.txt
uv sync
```

### 3.4 创建虚拟环境

```
uv venv
```



------

## 4. 依赖管理

### 4.1 添加依赖（add）

```bash
# 添加单个依赖
uv add requests

# 添加指定版本
uv add "requests>=2.28,<3.0"
uv add "flask==3.0.*"

# 一次添加多个
uv add requests flask fastapi

# 添加 Git 依赖
uv add "git+https://github.com/psf/requests.git"

# 添加带有 extras 的依赖
uv add "requests[security]"

uv add -r requirements.txt

uv pip install 
# 缺点 无法自动添加到pyproject.toml文件中 只会添加到当前环境中。
```

执行 `uv add` 后，uv 会同时：

1. 更新 `pyproject.toml` 中的依赖声明
2. 更新 `uv.lock` 锁文件
3. 安装到 `.venv` 虚拟环境中

### 4.2 移除依赖（remove）

```bash
uv remove requests
uv remove flask fastapi
```

### 4.3 开发依赖（--dev）

```bash
# 添加开发依赖（如测试、lint 工具）
uv add --dev pytest ruff mypy

# 等价于
uv add -d pytest ruff mypy
```

开发依赖会记录在 `pyproject.toml` 的 `[dependency-groups]` 下的 `dev` 组中：

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
    "mypy>=1.10",
]
```

### 4.4 自定义依赖组（--group）

uv 支持自定义命名的依赖组，便于分类管理：

```bash
# 创建 "test" 组
uv add --group test pytest pytest-cov

# 创建 "docs" 组
uv add --group docs sphinx sphinx-rtd-theme

# 创建 "lint" 组
uv add --group lint ruff black
```

对应 `pyproject.toml`：

```toml
[dependency-groups]
dev = ["pytest>=8.0"]
test = ["pytest>=8.0", "pytest-cov>=5.0"]
docs = ["sphinx>=7.0", "sphinx-rtd-theme>=2.0"]
lint = ["ruff>=0.4", "black>=24.0"]
```

**同步时排除/包含特定组：**

```bash
# 同步时不包含 docs 组
uv sync --no-group docs

# 仅安装某个组
uv sync --group test
```

### 4.5 查看依赖树（tree）

```bash
# 显示项目的完整依赖树
uv tree

# 以 JSON 格式输出
uv tree --json

# 反向依赖树（谁依赖了某个包）
uv tree --invert

# 只显示到第 2 层
uv tree --depth 2

# 显示指定包的依赖树
uv tree --package requests
```

### 4.6 依赖覆盖（override）*

当你需要强制某个传递依赖使用特定版本时，可以使用 `override`。

**在 `pyproject.toml` 中声明：**

```toml
[tool.uv]
override-dependencies = [
    "numpy==1.26.4",           # 强制所有 numpy 使用此版本
    "urllib3<2.0",             # 强制限制 urllib3 版本
]
```

**使用单独的 override 文件：**

```bash
# 创建 overrides.txt（格式同 requirements.txt）
echo "numpy==1.26.4" > overrides.txt
echo "urllib3<2.0" >> overrides.txt

# 通过环境变量指定 override 文件
UV_OVERRIDE=overrides.txt uv sync
```

**在 `pyproject.toml` 中引用 override 文件：**

```toml
[tool.uv]
override-dependencies = [
    "numpy==1.26.4",
]
# 或从文件读取
# 在 uv 中使用 constraint-dependencies 也可达到类似效果
constraint-dependencies = [
    "requests>=2.28",
]
```

------

## 5. 环境同步与锁文件

### 5.1 锁文件（uv.lock）

uv 使用 `uv.lock` 文件来锁定所有依赖的精确版本（包括传递依赖），确保可复现的构建。

```bash
# 生成 / 更新锁文件
uv lock

# 查看锁文件的变动（dry-run）
uv lock --check
```

> ⚠️ **请将 `uv.lock` 提交到版本控制**，这是团队协作和 CI/CD 可复现性的关键。

### 5.2 同步环境（sync）

`uv sync` 是核心命令，它根据 `pyproject.toml` 和 `uv.lock` 将虚拟环境同步到一致状态。

```bash
# 基础同步 — 安装所有依赖，自动创建 .venv
uv sync

# 同步时更新锁文件*
uv sync --update
```

### 5.3 --frozen 模式

```bash
# 使用已有的 uv.lock，不更新锁文件
uv sync --frozen
```

**适用场景：** CI/CD 中你希望确保锁文件不会被意外修改，如果锁文件过期则直接报错。

### 5.4 --locked 模式

```bash
# 验证锁文件与 pyproject.toml 一致，不做任何修改
uv sync --locked
```

**适用场景：** CI 中验证锁文件是否最新——如果 `pyproject.toml` 已修改但锁文件未更新，此命令会失败。

**三种模式对比：**

| 模式               | 更新锁文件？ | 锁文件不存在？ | 锁文件过期？ |
| ------------------ | ------------ | -------------- | ------------ |
| `uv sync`          | ✅ 自动更新   | 自动创建       | 自动更新     |
| `uv sync --frozen` | ❌ 不更新     | ❌ 报错         | ❌ 报错       |
| `uv sync --locked` | ❌ 不更新     | ❌ 报错         | ❌ 报错       |

### 5.5 其他同步选项

```bash
# 不包含开发依赖
uv sync --no-dev

# 不包含特定依赖组
uv sync --no-group docs

# 重新安装所有包（忽略缓存）
uv sync --reinstall

# 重新安装特定包
uv sync --reinstall-package requests

# 排除某个包的安装
uv sync --no-install-package setuptools
```

### 5.6 缓存机制

uv 拥有全局缓存系统，极大加速后续安装：

```bash
# 查看缓存目录和大小
uv cache dir

# 清除所有缓存
uv cache clean

# 清除特定包的缓存
uv cache clean requests

# 同步时跳过缓存（强制从网络获取）
uv sync --no-cache
```

**缓存原理：**

- uv 使用 **全局内容寻址缓存**（类似 Git 的对象存储）
- 下载的包通过哈希值存储，不同项目共享同一份缓存
- 多个项目使用相同版本的包时，不会重复下载
- 缓存目录默认位于 `~/.cache/uv`（Linux/macOS）或 `%LOCALAPPDATA%\uv\cache`（Windows）

------

## 6. 运行与任务

### 6.1 uv run — 运行脚本和命令

`uv run` 在项目虚拟环境中执行命令，自动确保环境是最新的：

```bash
# 运行 Python 脚本
uv run python main.py

# 直接运行脚本（uv 自动使用正确的 Python）
uv run main.py

# 运行项目中的 CLI 工具
uv run ruff check .
uv run pytest tests/

# 运行交互式 Python REPL
uv run python

# 传递参数
uv run python main.py --config prod.yaml --verbose
```

**`uv run` 的智能行为：**

- 自动创建 `.venv`（如果不存在）
- 自动安装/更新依赖（如果 `pyproject.toml` 有变化）
- 自动使用 `.python-version` 指定的 Python 版本

### 6.2 带临时依赖运行

```bash
# 运行时临时安装依赖（不修改 pyproject.toml）
uv run --with requests --with flask python script.py

# 指定版本
uv run --with "pandas>=2.0" python analyze.py
```

### 6.3 uvx — 运行一次性工具（替代 pipx）

`uvx` 是 `uv tool run` 的快捷命令，在临时隔离环境中运行 Python CLI 工具，**无需预先安装**：

```bash
# 直接运行 ruff（自动下载、运行、清理）
uvx ruff check .

# 运行 httpie
uvx httpie GET https://httpbin.org/get

# 运行 black 格式化代码
uvx black .

# 指定版本
uvx ruff@0.4.0 check .

# 带额外依赖
uvx --with requests python -c "import requests; print(requests.__version__)"
```

**永久安装工具：**

```bash
# 安装工具到全局（类似 pipx install）
uv tool install ruff
uv tool install httpie

# 列出已安装的工具
uv tool list

# 升级工具
uv tool upgrade ruff

# 卸载工具
uv tool uninstall ruff

# 升级所有工具
uv tool upgrade --all
```

## 速查表

| 场景             | 命令                                              |
| ---------------- | ------------------------------------------------- |
| 安装 uv          | `curl -LsSf https://astral.sh/uv/install.sh | sh` |
| 升级 uv          | `uv self update`                                  |
| 安装 Python      | `uv python install 3.12`                          |
| 固定 Python 版本 | `uv python pin 3.12`                              |
| 新建项目         | `uv init my-project`                              |
| 新建库项目       | `uv init --lib my-lib`                            |
| 添加依赖         | `uv add requests`                                 |
| 添加开发依赖     | `uv add --dev pytest`                             |
| 添加自定义组     | `uv add --group docs sphinx`                      |
| 移除依赖         | `uv remove requests`                              |
| 查看依赖树       | `uv tree`                                         |
| 同步环境         | `uv sync`                                         |
| CI 同步（严格）  | `uv sync --locked`                                |
| 运行脚本         | `uv run python main.py`                           |
| 运行一次性工具   | `uvx ruff check .`                                |
| 安装全局工具     | `uv tool install ruff`                            |
| 运行内联脚本     | `uv run script.py`                                |
| 清除缓存         | `uv cache clean`                                  |