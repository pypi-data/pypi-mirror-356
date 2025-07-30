from setuptools import setup, find_packages
import os

# 读取README.md内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EnigmaEnhanced",
    version="0.1.1",
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
            'enigmaenhanced = cli:main',
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