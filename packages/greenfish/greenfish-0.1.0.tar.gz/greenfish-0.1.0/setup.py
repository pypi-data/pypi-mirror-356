import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="greenfish",
    version="0.1.0",
    author="Yusef Ulum",
    author_email="yusef314159@gmail.com",
    description="A Redfish and IPMI desktop client for out-of-band server management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mexyusef/greenfish",
    project_urls={
        "Bug Tracker": "https://github.com/mexyusef/greenfish/issues",
        # "Documentation": "https://greenfish.readthedocs.io",
        "Source Code": "https://github.com/mexyusef/greenfish",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    packages=find_packages(where="greenfish"),
    package_dir={"": "greenfish"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "greenfish-cli=greenfish.main:main",
            "greenfish=greenfish.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
