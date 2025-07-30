from setuptools import setup, find_packages
import os
import re

# 读取README.md内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 从 __init__.py 读取版本号
def get_version():
    init_file = os.path.join(os.path.dirname(__file__), 'EnigmaEnhanced', '__init__.py')
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("无法找到版本信息 | Unable to find version string.")

setup(
    name="EnigmaEnhanced",
    version=get_version(),
    author="PaulLiszt",
    author_email="paullizst@gmail.com",
    description="Enhanced Enigma Cipher Machine with modern cryptographic techniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PaulLiszt/EnigmaEnhanced",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'enigmaenhanced = EnigmaEnhanced.cli:main',  # 更新为 EnigmaEnhanced.cli
        ],
    },
    install_requires=[],
    keywords="enigma cipher cryptography encryption decryption",
    project_urls={
        "Source Code": "https://github.com/PaulLiszt/EnigmaEnhanced",
        "Bug Tracker": "https://github.com/PaulLiszt/EnigmaEnhanced/issues",
    },
    license="MIT",
)