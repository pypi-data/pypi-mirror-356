# Powechi 包发布指南

## 准备工作

### 1. 注册 PyPI 账户

1. 访问 [PyPI](https://pypi.org/) 并注册账户
2. 访问 [TestPyPI](https://test.pypi.org/) 并注册账户（用于测试）
3. 启用两步验证（推荐）

### 2. 创建 API Token

1. 登录 PyPI，进入 Account settings
2. 在 API tokens 部分创建新的 token
3. 选择 "Entire account" 或指定项目
4. 保存生成的 token（格式：`pypi-...`）

### 3. 配置认证

创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-你的API令牌

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-你的TestPyPI API令牌
```

## 发布流程

### 1. 安装发布工具

```bash
pip install build twine
```

或者安装开发依赖：

```bash
make install-dev
```

### 2. 更新版本号

在以下文件中更新版本号：
- `setup.py`
- `pyproject.toml`
- `powechi/__init__.py`

### 3. 运行测试

```bash
make test
```

### 4. 代码检查和格式化

```bash
make lint
make format
```

### 5. 构建包

```bash
make build
```

这会在 `dist/` 目录下生成：
- `powechi-x.x.x.tar.gz` (源代码分发)
- `powechi-x.x.x-py3-none-any.whl` (wheel 分发)

### 6. 测试发布（推荐）

首先发布到 TestPyPI：

```bash
make upload-test
```

然后测试安装：

```bash
pip install --index-url https://test.pypi.org/simple/ powechi
```

### 7. 正式发布

确认测试无误后，发布到正式 PyPI：

```bash
make upload
```

### 8. 验证发布

```bash
pip install powechi
```

## 自动化发布（GitHub Actions）

可以设置 GitHub Actions 来自动化发布流程。创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

需要在 GitHub 仓库的 Settings > Secrets 中添加 `PYPI_API_TOKEN`。

## 版本管理建议

1. 遵循 [语义化版本](https://semver.org/lang/zh-CN/)
2. 主版本号：不兼容的 API 修改
3. 次版本号：向下兼容的功能性新增
4. 修订号：向下兼容的问题修正

## 常见问题

### 1. 包名已存在

如果包名 `powechi` 已被占用，需要选择其他名称或联系现有包的维护者。

### 2. 上传失败

- 检查网络连接
- 确认 API token 正确
- 确认版本号未重复

### 3. 权限问题

确保 API token 有足够的权限上传包。

## 维护建议

1. 定期更新依赖
2. 保持代码质量
3. 及时修复 bug
4. 响应用户反馈
5. 维护文档更新 