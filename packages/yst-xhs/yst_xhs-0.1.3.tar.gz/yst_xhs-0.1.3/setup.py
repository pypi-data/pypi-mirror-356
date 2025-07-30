from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="yst_xhs",
    version="0.1.3",  # 增加版本号
    author="yst",
    author_email="",
    description="小红书爬虫工具",
    # 问题出在这里，find_packages()可能找到了两层目录结构
    # packages=find_packages(),  # 这会找到所有包括yst_xhs.yst_xhs的包
    
    # 替换为以下方式之一:
    packages=["yst_xhs", "yst_xhs.apis", "yst_xhs.xhs_utils"],  # 方法1：明确指定包
    # 或者
    # packages=find_packages(exclude=["yst_xhs.yst_xhs*"]),  # 方法2：排除嵌套目录
    
    include_package_data=True,
    package_data={
        'yst_xhs': ['static/*.js'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'yst_xhs=yst_xhs.main:main',
        ],
    },
)
