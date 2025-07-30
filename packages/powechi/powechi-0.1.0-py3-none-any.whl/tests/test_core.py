"""
测试 powechi.core 模块
"""

import pytest
from powechi.core import hello, add, multiply


def test_hello_default():
    """测试默认问候"""
    result = hello()
    assert result == "Hello, World!"


def test_hello_with_name():
    """测试带名字的问候"""
    result = hello("Alice")
    assert result == "Hello, Alice!"


def test_hello_with_chinese_name():
    """测试中文名字的问候"""
    result = hello("小明")
    assert result == "Hello, 小明!"


def test_add():
    """测试加法函数"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_multiply():
    """测试乘法函数"""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0


def test_add_large_numbers():
    """测试大数加法"""
    assert add(1000000, 2000000) == 3000000


def test_multiply_large_numbers():
    """测试大数乘法"""
    assert multiply(1000, 2000) == 2000000 