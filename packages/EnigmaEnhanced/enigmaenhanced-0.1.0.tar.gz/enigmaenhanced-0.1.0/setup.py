from setuptools import setup, find_packages

setup(
    name="EnigmaEnhanced",      # PyPI 显示的包名（全局唯一）
    version="0.1.0",               # 版本号（遵循语义化版本）
    author="PaulLiszt",
    author_email="paullizst@gmail.com",
    description="Enhanced Enigma Cipher Machine - Python Implementation",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PaulLiszt/EnigmaEnhanced",
    packages=find_packages(),      # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',      # Python 版本要求
    install_requires=[],           # 依赖包列表（如 ["requests>=2.25"]）
)