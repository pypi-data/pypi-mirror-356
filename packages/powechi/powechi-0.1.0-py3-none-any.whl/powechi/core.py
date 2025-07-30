"""
Powechi 核心功能模块
"""

# 不需要导入 str，它是内置类型


def hello(name: str = "World") -> str:
    """
    简单的问候函数
    
    Args:
        name: 要问候的名字，默认为 "World"
        
    Returns:
        问候语字符串
        
    Example:
        >>> hello("Alice")
        'Hello, Alice!'
        >>> hello()
        'Hello, World!'
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """
    两个数相加
    
    Args:
        a: 第一个数
        b: 第二个数
        
    Returns:
        两数之和
        
    Example:
        >>> add(2, 3)
        5
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """
    两个数相乘
    
    Args:
        a: 第一个数
        b: 第二个数
        
    Returns:
        两数之积
        
    Example:
        >>> multiply(3, 4)
        12
    """
    return a * b 