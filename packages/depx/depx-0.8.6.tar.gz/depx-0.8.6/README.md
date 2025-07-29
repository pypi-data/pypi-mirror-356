# Depx - 本地多语言依赖统一管理器

🚀 **统一发现 • 信息透明 • 空间优化 • 跨平台支持**

Depx 是一个强大的本地依赖管理工具，能够自动识别和分析本地文件系统中各种编程语言项目的依赖关系，帮助开发者更好地管理和优化项目依赖。

## ✨ 核心特性

### 🔍 统一发现
- 自动识别本地文件系统中的各类编程语言项目
- 支持 Node.js、Python、Java、Go、Rust 等多种语言（逐步支持）
- 智能扫描项目配置文件和依赖目录

### 📊 信息透明
- 提供依赖的详细信息：名称、版本、大小、位置
- 清晰展示项目依赖关系和层级结构
- 支持多种排序和筛选方式
- 多格式导出：JSON、CSV、HTML

### 💾 空间优化
- 识别重复和冗余的依赖
- 计算精确的磁盘占用空间
- 智能清理开发依赖和缓存
- 安全的依赖清理功能

### 🌐 跨平台支持
- 在 Windows、macOS 和 Linux 上稳定运行
- 统一的命令行界面
- 美观的输出格式

## 🚀 快速开始

### 🎯 一键运行（推荐）

无需安装，直接运行：

#### Linux/macOS
```bash
curl -fsSL https://raw.githubusercontent.com/NekoNuo/depx/master/install_and_run.sh | bash
```

#### Windows PowerShell
```powershell
irm https://raw.githubusercontent.com/NekoNuo/depx/master/install_and_run.ps1 | iex
```

这些脚本会自动：
- ✅ 检查系统环境
- ✅ 下载最新版本
- ✅ 安装必要依赖
- ✅ 提供交互界面
- ✅ 使用完毕后自动清理

### 本地运行方式

如果已下载项目，可以使用以下方式：

#### 方式一：一键启动（推荐新手）
```bash
python quick_start.py
```
自动检查环境、安装依赖，提供多种运行选择。

#### 方式二：交互式界面（推荐新手）
```bash
python interactive_depx.py
```
友好的菜单界面，逐步引导操作：
- 📊 分析项目依赖
- 🔍 搜索包
- 📦 安装/卸载包
- 🔄 更新包
- 🌐 扫描全局依赖

#### 方式三：直接命令行（推荐专家）
```bash
# 查看帮助
python run_depx.py --help

# 分析当前项目
python run_depx.py info .

# 搜索包
python run_depx.py search lodash

# 安装包
python run_depx.py install express

# 更新包
python run_depx.py update --check
```

### 安装

#### 从 PyPI 安装（推荐）

```bash
# 安装 Depx
pip install depx

# 验证安装
depx --version
```

#### 从源码安装

```bash
# 克隆项目
git clone <repository-url>
cd depx

# 安装依赖
pip install -r requirements.txt

# 安装 Depx
pip install -e .
```

### 基本使用

```bash
# 扫描当前目录的项目
depx scan

# 扫描指定目录
depx scan /path/to/projects

# 分析依赖并生成详细报告
depx analyze

# 查看单个项目的详细信息
depx info /path/to/project

# 扫描系统全局依赖
depx global-deps

# 清理开发依赖和缓存（新功能）
depx clean . --type dev cache --dry-run

# 导出分析结果（新功能）
depx export . --format json --type projects

# 管理配置文件（新功能）
depx config --create
depx config --show

# 查看帮助
depx --help
```

### 快速示例

```bash
# 1. 扫描你的项目目录
depx scan ~/projects

# 2. 分析依赖，查看重复和清理建议
depx analyze ~/projects

# 3. 查看全局安装的 npm 包
depx global-deps --type npm --sort-by size

# 4. 查看特定项目的详细信息
depx info ~/projects/my-app
```

## 📋 命令详解

### `depx scan` - 项目扫描

扫描指定目录，发现所有支持的项目类型。

```bash
# 基本扫描（扫描当前目录）
depx scan

# 扫描指定目录
depx scan /path/to/projects

# 指定扫描深度（默认5层）
depx scan --depth 3

# 只扫描特定类型的项目
depx scan --type nodejs
depx scan --type nodejs --type python

# 禁用并行处理（默认启用）
depx scan --no-parallel

# 启用详细输出
depx scan --verbose
```

**输出示例：**
```
🔍 扫描目录: /Users/user/projects
📏 扫描深度: 5
⚡ 并行处理: 启用

✅ 发现 2 个项目
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ 项目名称               ┃ 类型   ┃ 路径                         ┃ 依赖数量 ┃  总大小 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ my-react-app           │ nodejs │ /Users/user/projects/react   │       15 │ 45.2 MB │
│ my-vue-app             │ nodejs │ /Users/user/projects/vue     │       12 │ 38.1 MB │
└────────────────────────┴────────┴──────────────────────────────┴──────────┴─────────┘
```

### `depx analyze` - 依赖分析

深度分析项目依赖，生成详细报告包括重复依赖检测和清理建议。

```bash
# 基本分析（分析当前目录）
depx analyze

# 分析指定目录
depx analyze /path/to/projects

# 指定扫描深度
depx analyze --depth 3

# 按不同方式排序
depx analyze --sort-by size    # 按大小排序（默认）
depx analyze --sort-by name    # 按名称排序
depx analyze --sort-by type    # 按类型排序

# 限制显示数量
depx analyze --limit 10
```

**输出示例：**
```
📊 总览
📊 总项目数: 2
📦 总依赖数: 27
💾 总占用空间: 83.3 MB

🔥 占用空间最大的依赖
┏━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ 依赖名称    ┃     大小 ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ webpack     │  15.2 MB │
│ typescript  │  12.8 MB │
│ react       │   8.1 MB │
└─────────────┴──────────┘

🔄 重复依赖
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ 依赖名称 ┃ 项目数 ┃ 版本数 ┃   总大小 ┃   可节省 ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ lodash   │      2 │      1 │   5.2 MB │   2.6 MB │
│ axios    │      2 │      2 │   4.8 MB │   2.1 MB │
└──────────┴────────┴────────┴──────────┴──────────┘

💡 清理建议
• 清理开发依赖: 开发依赖在生产环境中不需要，可以考虑清理
  潜在节省: 25.4 MB
```

### `depx info` - 项目信息

显示单个项目的详细信息，包括所有依赖的详细列表。

```bash
# 查看项目信息
depx info /path/to/project

# 查看当前目录项目信息
depx info .
```

**输出示例：**
```
📋 项目信息
📁 项目名称: my-react-app
🏷️  项目类型: nodejs
📍 项目路径: /Users/user/projects/react
⚙️  配置文件: /Users/user/projects/react/package.json
📦 依赖数量: 15
💾 总大小: 45.2 MB

📦 依赖列表
┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ 名称        ┃ 版本    ┃ 类型        ┃     大小 ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ react       │ 18.2.0  │ production  │   8.1 MB │
│ webpack     │ 5.89.0  │ development │  15.2 MB │
│ typescript  │ 5.3.0   │ development │  12.8 MB │
└─────────────┴─────────┴─────────────┴──────────┘
```

### `depx global-deps` - 全局依赖

扫描和显示系统中全局安装的依赖，支持多种包管理器。

```bash
# 扫描所有全局依赖
depx global-deps

# 只扫描特定包管理器的全局依赖
depx global-deps --type npm
depx global-deps --type pip
depx global-deps --type yarn

# 按不同方式排序
depx global-deps --sort-by size     # 按大小排序（默认）
depx global-deps --sort-by name     # 按名称排序
depx global-deps --sort-by manager  # 按包管理器排序

# 限制显示数量
depx global-deps --limit 20

# 组合使用
depx global-deps --type npm --sort-by size --limit 10
```

**输出示例：**
```
🌍 扫描全局依赖...
✅ 发现 83 个全局依赖
📦 检测到的包管理器: npm, pip

🌍 全局依赖
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 依赖名称         ┃ 版本    ┃ 包管理器 ┃    大小 ┃ 安装路径                                           ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ typescript       │ 5.3.0   │ npm      │ 21.8 MB │ /usr/local/lib/node_modules/typescript            │
│ @vue/cli         │ 5.0.8   │ npm      │ 18.2 MB │ /usr/local/lib/node_modules/@vue/cli               │
│ create-react-app │ 5.0.1   │ npm      │ 15.1 MB │ /usr/local/lib/node_modules/create-react-app       │
│ requests         │ 2.31.0  │ pip      │     0 B │ 未知                                               │
│ numpy            │ 1.24.0  │ pip      │     0 B │ 未知                                               │
└──────────────────┴─────────┴──────────┴─────────┴────────────────────────────────────────────────────┘
```

### 通用选项

所有命令都支持以下通用选项：

```bash
# 查看版本
depx --version

# 启用详细输出（显示调试信息）
depx --verbose scan
depx -v analyze

# 查看帮助
depx --help
depx scan --help
depx analyze --help
depx info --help
depx global-deps --help
```

## 🏗️ 项目结构

```
depx/
├── depx/
│   ├── __init__.py
│   ├── cli.py              # 命令行入口
│   ├── core/
│   │   ├── scanner.py      # 项目扫描器
│   │   └── analyzer.py     # 依赖分析器
│   ├── parsers/
│   │   ├── base.py         # 基础解析器
│   │   └── nodejs.py       # Node.js 解析器
│   └── utils/
│       └── file_utils.py   # 文件工具
├── tests/                  # 测试文件
├── requirements.txt        # Python 依赖
└── setup.py               # 安装配置
```

## 🎯 当前支持

### ✅ 已支持
- **Node.js**: package.json, node_modules, npm/yarn/pnpm
- **Python**: requirements.txt, setup.py, pyproject.toml, Pipfile, venv
- **Java**: pom.xml (Maven), build.gradle (Gradle) 🆕
- **Go**: go.mod, go.sum, Gopkg.toml 🆕
- **Rust**: Cargo.toml, Cargo.lock 🆕
- **PHP**: composer.json, composer.lock 🆕
- **C#**: .csproj, packages.config, project.json 🆕
- **全局依赖**: npm 全局包、pip 全局包、yarn 全局包
- **依赖清理**: 开发依赖、缓存文件、大型依赖
- **导出功能**: JSON、CSV、HTML 格式
- **配置管理**: YAML 配置文件支持

### 🚧 计划支持
- **Ruby**: Gemfile, Gemfile.lock
- **Swift**: Package.swift
- **Kotlin**: build.gradle.kts
- **Dart**: pubspec.yaml
- **Scala**: build.sbt
- **Haskell**: cabal, stack.yaml
- **依赖安全扫描**: 检查已知漏洞
- **依赖更新检查**: 检查过时的依赖

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_scanner.py

# 运行测试并显示覆盖率
pytest --cov=depx
```

## 📦 发布到 PyPI

### 自动发布（推荐）

项目配置了 GitHub Actions 自动发布流程：

#### 🧪 测试发布（TestPyPI）
```bash
# 推送标签触发测试发布
git tag v0.4.0
git push origin v0.4.0

# 结果：发布到 TestPyPI，不会发布到正式 PyPI
```

#### 🚀 正式发布（PyPI）
```bash
# 方式 1: 创建 GitHub Release（推荐）
# 在 GitHub 上创建 Release，自动发布到 PyPI

# 方式 2: 手动触发工作流
# 在 Actions 页面手动运行，选择 "Publish to PyPI: true"
```

#### 🔧 配置 Secrets
在 GitHub 仓库设置中添加以下 Secrets：
- `PYPI_API_TOKEN`: PyPI API Token
- `TEST_PYPI_API_TOKEN`: TestPyPI API Token

详细发布指南请查看 [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)

### 手动发布

```bash
# 1. 确保所有测试通过
python -m pytest tests/ -v

# 2. 更新版本号（在 pyproject.toml、setup.py 和 __init__.py 中）
# 3. 构建包
python -m build

# 4. 检查包
python -m twine check dist/*

# 5. 上传到 TestPyPI（测试）
python -m twine upload --repository testpypi dist/*

# 6. 测试安装
pip install --index-url https://test.pypi.org/simple/ depx

# 7. 上传到 PyPI（正式发布）
python -m twine upload dist/*
```

### 安装构建工具

```bash
pip install build twine
```

## 🤝 贡献指南

我们欢迎各种形式的贡献！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/depx.git
cd depx

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/ -v --cov=depx
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🗺️ 开发路线图

### v0.4.0 (当前) 🎉
- ✅ 基础架构搭建
- ✅ Node.js 项目支持
- ✅ Python 项目支持 🆕
- ✅ 全局依赖扫描 (npm, pip, yarn)
- ✅ 依赖清理功能 🆕
- ✅ 多格式导出 (JSON, CSV, HTML) 🆕
- ✅ 配置文件支持 (YAML) 🆕
- ✅ 完整的命令行界面
- ✅ 全面的测试覆盖
- ✅ GitHub Actions CI/CD
- ✅ PyPI 自动发布

### v0.9.0 (计划中)
- 🚧 Java/Maven/Gradle 支持
- 🚧 Go 项目支持
- 🚧 依赖安全扫描
- 🚧 依赖更新检查
- 🚧 性能优化

### v0.10.0 (未来)
- 🔮 Rust 项目支持
- 🔮 PHP 项目支持
- 🔮 Web 界面 (可选)
- 🔮 插件系统

## 📞 联系我们

如果您有任何问题或建议，请通过以下方式联系我们：

- 提交 Issue
- 发起 Discussion
- 发送邮件

---

**Depx** - 让依赖管理变得简单高效！ 🎉