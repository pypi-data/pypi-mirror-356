"""
Setup configuration for LemonMeringue package
"""

from setuptools import setup, find_packages
import os

# Read the README file
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open(os.path.join(current_dir, "requirements.txt"), "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lemonmeringue",
    version="0.1.3",
    author="Neel Datta",
    author_email="neeldatta@berkeley.edu",
    description="Enhanced Python SDK for LemonSlice API with retry logic and better error handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neeldatta/lemonmeringue",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Video :: Display",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="lemonslice api video generation ai lip-sync sdk wrapper",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=5.0",
            "mypy>=1.0",
            "twine>=4.0",
            "build>=0.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "lemonmeringue=lemonmeringue.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/neeldatta/lemonmeringue/issues",
        "Source": "https://github.com/neeldatta/lemonmeringue",
        "Documentation": "https://github.com/neeldatta/lemonmeringue#readme",
    },
)