# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:15:25 2025

@author: 2
"""

from setuptools import setup

setup(
    name="cehuibaibaoxiang",  # 你的库名称（在 PyPI 上的名称）
    version="0.1.0",          # 版本号
    author="徐若朴",       # 你的名字
    author_email="2253959@tongji.edu.cn",  # 你的邮箱
    description="（自用）同济大学测绘学院专业课代码合集",  # 简短描述
    long_description=open("README.md",encoding="utf-8").read(),  # 读取 README.md 文件内容作为详细描述
    long_description_content_type="text/markdown",  # 指定 README.md 文件类型为 Markdown
    url="https://github.com/your_username/your_project",  # 项目主页（如果有）
    license="MIT",  # 许可证类型
    py_modules=["cehuibaibaoxiang"],  # 指定要打包的 Python 文件（不包含扩展名）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "gdal",
        "scipy",
        "pandas",
        "opencv-python",
    ],
    python_requires=">=3.8",  # Python 版本要求
)