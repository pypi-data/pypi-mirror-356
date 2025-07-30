#!/usr/bin/env python3
# encoding: utf-8
from setuptools import setup, find_packages
import os

__version__ = "0.8.0"
__desc__ = "Convert markdown to html with TOC(table of contents) and Mermaid diagram support"

repo_url = "https://github.com/ltto/mdtree"

# 读取README文件作为长描述
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return __desc__

setup(
    name="mdtree-mermaid",
    version=__version__,
    keywords=["markdown", "toc", "tree", "html", "mermaid", "documentation", "converter"],
    description=__desc__,
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    url=repo_url,
    project_urls={
        "Bug Reports": f"{repo_url}/issues",
        "Source": repo_url,
        "Documentation": repo_url,
    },
    author="menduo",
    author_email="shimenduo@gmail.com",
    packages=find_packages(),
    package_data={
        "mdtree": [
            "static/css/*.css",
            "static/js/*.js", 
            "static/html/*.html",
        ]
    },
    include_package_data=True,
    scripts=["bin/mdtree"],
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    install_requires=[
        "markdown>=3.0",
        "pygments>=2.0", 
        "markdown-mermaidjs>=1.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mdtree=mdtree.main:main",
        ],
    },
)
