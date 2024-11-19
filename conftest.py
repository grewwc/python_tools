# conftest.py
import sys
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前工作目录添加到 PYTHONPATH
sys.path.insert(0, current_dir)