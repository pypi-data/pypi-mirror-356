# Powechi

一个强大的 Python 实用工具库。

## 安装

```bash
pip install powechi
```

## 快速开始

```python
from powechi import hello

# 使用示例
result = hello("World")
print(result)  # 输出: Hello, World!
```

## 功能特性

- 简单易用的 API
- 高性能
- 完整的类型提示支持
- 全面的测试覆盖

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black powechi/
```

### 类型检查

```bash
mypy powechi/
```

## 许可证

MIT License

## 贡献

欢迎提交 Pull Request 和 Issue！

## 更新日志

### 0.1.0 (2024-01-01)

- 初始版本发布
- 基础功能实现 