from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flatten-cli",
    version="1.0.0",
    author="PaxtonTerryDev",
    author_email="paxtonterrydev@gmail.com",
    description="A CLI tool to flatten directory structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PaxtonTerryDev/flatten",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "flatten=flatten.cli:main",
        ],
    },
    keywords="cli directory flatten filesystem developer-tools",
)