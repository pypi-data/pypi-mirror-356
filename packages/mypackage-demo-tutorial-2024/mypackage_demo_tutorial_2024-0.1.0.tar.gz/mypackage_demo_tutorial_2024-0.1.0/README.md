# 如何创建Python库完整教程

这是一个完整的Python库创建教程，从零开始教你如何创建、构建和分发一个Python包。

## 📚 教程目标

学会创建一个名为 `mypackage` 的Python库，提供 `add_one` 函数，并能够通过pip安装。

## 🎯 最终效果

```python
from mypackage import add_one
print(add_one(5))    # 输出: 6
print(add_one(2.5))  # 输出: 3.5
```

## 📖 详细步骤教程

### 第1步：创建项目目录结构

**目标**: 建立标准的Python包目录结构

**具体操作**:
```bash
# 1. 创建项目根目录
mkdir mypackage-project
cd mypackage-project

# 2. 创建源码目录
mkdir src

# 3. 创建包目录
mkdir src\mypackage
```

**结果验证**:
```
mypackage-project/
└── src/
    └── mypackage/
```

**关键知识点**:
- `src` 布局是现代Python项目的最佳实践
- 包名（`mypackage`）应该是有效的Python标识符
- 这种结构避免了测试时意外导入开发中的代码

### 第2步：编写核心功能代码

**目标**: 实现库的主要功能

**创建文件**: `src/mypackage/utils.py`
```python
def add_one(number):
    """
    接收一个数字并返回加一后的结果
    
    Args:
        number: 输入的数字 (int 或 float)
        
    Returns:
        输入数字加1后的结果
        
    Examples:
        >>> add_one(5)
        6
        >>> add_one(2.5)
        3.5
    """
    return number + 1
```

**关键知识点**:
- 函数要有清晰的文档字符串(docstring)
- 使用类型提示可以提高代码质量
- 模块文件名应该简洁明了

### 第3步：定义包的公共API

**目标**: 让用户能够直接从包导入函数

**创建文件**: `src/mypackage/__init__.py`
```python
"""
mypackage - 一个简单的Python库示例

提供基本的数学工具函数。
"""

from .utils import add_one

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# 定义公共API
__all__ = ["add_one"]
```

**关键知识点**:
- `__init__.py` 使目录成为Python包
- `from .utils import add_one` 将内部函数暴露给用户
- `__all__` 定义了 `from mypackage import *` 时导入的内容
- `__version__` 是包版本的标准位置

### 第4步：创建项目配置文件

**目标**: 告诉Python如何构建和安装这个包

**创建文件**: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage-example"
version = "0.1.0"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
description = "一个简单的Python库示例，提供基本数学工具函数"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.7"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
keywords = ["math", "utility", "example"]

[project.urls]
"Homepage" = "https://github.com/yourusername/mypackage-example"
"Bug Tracker" = "https://github.com/yourusername/mypackage-example/issues"

[tool.setuptools.packages.find]
where = ["src"]
include = ["mypackage*"]
```

**关键知识点**:
- `pyproject.toml` 是现代Python项目的标准配置文件
- `build-system` 指定构建工具
- `project` 部分包含包的元数据
- `tool.setuptools.packages.find` 告诉setuptools在哪里找到包
- `classifiers` 帮助PyPI用户分类查找你的包

### 第5步：添加项目文档

**目标**: 提供项目说明和使用许可

**创建文件**: `LICENSE`
```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**关键知识点**:
- 许可证文件是开源项目的必需品
- MIT许可证是最宽松的开源许可证之一
- 许可证要与pyproject.toml中的声明一致

### 第6步：构建包

**目标**: 将源码打包成可分发的格式

**具体操作**:
```bash
# 1. 安装构建工具
python -m pip install build

# 2. 构建包（在项目根目录运行）
python -m build
```

**命令解释**:
- `python -m build` 会创建两种分发格式：
  - `.whl` (Wheel): 二进制分发格式，安装更快
  - `.tar.gz` (Source): 源码分发格式，兼容性更好

**结果验证**:
构建完成后会生成 `dist/` 目录：
```
dist/
├── mypackage_example-0.1.0-py3-none-any.whl
└── mypackage_example-0.1.0.tar.gz
```

**关键知识点**:
- 构建是将源码转换为可安装格式的过程
- Wheel格式是现代Python包分发的标准
- 文件名包含包名、版本号和兼容性信息

### 第7步：安装和测试

**目标**: 验证包是否正确构建和工作

**具体操作**:
```bash
# 1. 安装构建的包
python -m pip install dist/mypackage_example-0.1.0-py3-none-any.whl

# 2. 测试功能
python -c "from mypackage import add_one; print('测试结果:', add_one(10))"
```

**期望输出**:
```
测试结果: 11
```

**进阶测试**:
```python
# 在Python解释器中测试
python
>>> from mypackage import add_one
>>> add_one(5)
6
>>> add_one(2.5)
3.5
>>> help(add_one)  # 查看函数文档
```

## 🔄 完整的工作流程总结

1. **设计** → 确定包的功能和API
2. **结构** → 创建标准的目录结构
3. **编码** → 实现核心功能
4. **配置** → 编写pyproject.toml
5. **文档** → 添加README和LICENSE
6. **构建** → 使用python -m build打包
7. **测试** → 安装并验证功能

## 🛠️ 常用命令总结

```bash
# 开发阶段
mkdir mypackage-project && cd mypackage-project
mkdir src\mypackage

# 构建阶段
python -m pip install build
python -m build

# 测试阶段
python -m pip install dist/mypackage_example-0.1.0-py3-none-any.whl
python -c "from mypackage import add_one; print(add_one(10))"

# 清理（可选）
python -m pip uninstall mypackage-example
```

## 🚀 进阶技巧

### 1. 开发模式安装
```bash
# 安装为可编辑模式，代码修改后立即生效
pip install -e .
```

### 2. 添加依赖
在pyproject.toml中添加：
```toml
[project]
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]
```

### 3. 添加测试
```bash
# 创建测试目录
mkdir tests
# 添加测试文件
touch tests/test_utils.py
```

### 4. 发布到PyPI
```bash
# 安装上传工具
pip install twine

# 上传到测试PyPI
twine upload --repository testpypi dist/*

# 上传到正式PyPI
twine upload dist/*
```

## ❓ 常见问题

**Q: 为什么使用src布局？**
A: src布局确保测试时使用的是安装的包，而不是源码目录，避免了假阳性测试。

**Q: pyproject.toml vs setup.py的区别？**
A: pyproject.toml是现代标准，更清晰且支持多种构建后端；setup.py是传统方式。

**Q: 如何选择包名？**
A: 包名应该唯一、简洁、符合Python命名规范，建议先在PyPI搜索确认没有重名。

**Q: 版本号怎么管理？**
A: 建议遵循语义化版本（SemVer）：主版本.次版本.修订版本

## 📚 扩展学习

- [Python打包官方指南](https://packaging.python.org/)
- [Setuptools文档](https://setuptools.pypa.io/)
- [Wheel格式规范](https://peps.python.org/pep-0427/)
- [语义化版本](https://semver.org/)

恭喜！您现在已经掌握了完整的Python库创建流程！🎉 