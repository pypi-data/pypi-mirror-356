.PHONY: help clean test lint format build upload upload-test install-dev

help:
	@echo "可用命令:"
	@echo "  clean       - 清理构建文件"
	@echo "  test        - 运行测试"
	@echo "  lint        - 运行代码检查"
	@echo "  format      - 格式化代码"
	@echo "  build       - 构建包"
	@echo "  upload-test - 上传到 TestPyPI"
	@echo "  upload      - 上传到 PyPI"
	@echo "  install-dev - 安装开发依赖"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	pytest -v

lint:
	flake8 powechi/
	mypy powechi/

format:
	black powechi/ tests/

build: clean
	python -m build

upload-test: build
	python -m twine upload --repository testpypi dist/*

upload: build
	python -m twine upload dist/*

install-dev:
	pip install -e ".[dev]" 