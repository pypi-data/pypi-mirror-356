from setuptools import setup, find_packages
import os

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        return f.read()

# Read version from version.py
__version__ = "0.1.6"

setup(
    name="taskdaily",
    version=__version__,
    author="Nainesh Rabadiya",
    author_email="nkrabadiya@gmail.com",
    description="A flexible daily task management system with customizable templates",
    long_description=read("README.md") + "\n\n" + read("QUICKSTART.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/nainesh-rabadiya/taskdaily",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "PyYAML>=6.0.0",
        "rich>=10.0.0",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "daily=taskdaily.cli.main:main",
        ],
    },
    package_data={
        "taskdaily": [
            "templates/*.md",
            "templates/*.yaml",
        ],
    },
    include_package_data=True,
    keywords="task-management daily-tasks project-management productivity",
) 