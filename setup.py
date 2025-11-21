"""
OmniForge Setup
Installation configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="omniforge",
    version="1.0.0",
    author="OmniForge Team",
    author_email="info@omniforge.dev",
    description="The Absolute Upgrade Engine - Repository Analysis and Transformation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MASSIVEMAGNETICS/build_me",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "omniforge=src.cli:cli",
        ],
    },
    include_package_data=True,
    keywords="code-analysis security-scanner code-quality modernization refactoring",
    project_urls={
        "Bug Reports": "https://github.com/MASSIVEMAGNETICS/build_me/issues",
        "Source": "https://github.com/MASSIVEMAGNETICS/build_me",
        "Documentation": "https://github.com/MASSIVEMAGNETICS/build_me#readme",
    },
)
