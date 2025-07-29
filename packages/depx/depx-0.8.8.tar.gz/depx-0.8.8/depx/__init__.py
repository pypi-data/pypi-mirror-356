"""
Depx - 本地多语言依赖统一管理器

统一发现、信息透明、空间优化、跨平台支持
"""

# 从版本文件读取版本号
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from version import get_version
    __version__ = get_version()
except ImportError:
    # 如果无法导入版本文件，使用默认版本
    __version__ = "0.8.8"
__author__ = "Depx Team"
__description__ = "本地多语言依赖统一管理器"

from .core.analyzer import DependencyAnalyzer
from .core.global_scanner import GlobalScanner
from .core.scanner import ProjectScanner

__all__ = [
    "ProjectScanner",
    "DependencyAnalyzer",
    "GlobalScanner",
]
