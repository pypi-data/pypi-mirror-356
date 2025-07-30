# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:15:25 2025

@author: 2
"""

from setuptools import setup

setup(
    name="cehuibaibaoxiang",  
    version="0.1.4",         
    author="徐若朴",       
    author_email="2253959@tongji.edu.cn",  
    description="（自用）本人写的测绘专业课作业代码合集",  
    long_description=open("README.md",encoding="utf-8").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/piaopiaoxuruop/cehuibaibaoxiang/tree/main?tab=readme-ov-file",  
    license="MIT",  # 许可证类型
    py_modules=["cehuibaibaoxiang"],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    install_requires=[
        "numpy",  # 用于数学运算和数组操作
        "scipy",  # 用于科学计算，包括Delaunay三角剖分和griddata插值
        "matplotlib",  # 用于绘图
        "shapely",  # 用于几何操作
        "pyproj",  # 用于地理坐标转换
        "rasterio",  # 用于栅格数据操作
        "imageio",  # 用于图像读写
        "gdal",  # 用于地理空间数据处理
        "opencv-python",  # OpenCV的Python接口
        "pandas",  # 用于数据分析
    ],
    python_requires=">=3.8",  # Python 版本要求
)