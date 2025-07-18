from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="daily-task-tracker",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautiful and modern desktop task management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/daily-task-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "customtkinter>=5.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "task-tracker=task_tracker:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/daily-task-tracker/issues",
        "Source": "https://github.com/yourusername/daily-task-tracker",
        "Documentation": "https://github.com/yourusername/daily-task-tracker#readme",
    },
)