# -*- coding: utf-8 -*-
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")


with open("requirements.txt", "r") as fin:
    REQUIRED_PACKAGES = fin.read()

setup(
    name="sqlmate",
    version=open((HERE / "version.txt"), "r").read().strip(),
    url="https://github.com/JiehangXie/sqlmate",
    author="Jiehang Xie",
    author_email="xiejiehang@foxmail.com",
    license="MIT License",
    description="An Agent for SQL generation and data analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
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
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=REQUIRED_PACKAGES,
    entry_points={
        "console_scripts": [
            "sqlmate=sqlmate.cli:main",
        ],
    },
)
