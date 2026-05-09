#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-link-cn-analysis",
    version="1.0.0",
    author="Richard Zhao",
    author_email="richardzhao@ai.link.cn",
    description="全方位投资分析系统 - 支持港股、美股、新加坡股市、基金、ETF、期货和数字货币的分析和监控",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RicharZhaoyj/ai-link-cn",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "yfinance>=0.2.28",
        "ccxt>=4.0.0",
        "schedule>=1.2.0",
        "requests>=2.31.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-analysis=multi_market_analysis_system:main",
            "ai-monitor=market_monitor:main",
            "ai-optimizer=portfolio_optimizer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.json", "*.md"],
    },
)