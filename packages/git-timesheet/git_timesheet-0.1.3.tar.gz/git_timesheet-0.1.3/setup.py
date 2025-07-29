from setuptools import setup, find_packages

setup(
    name="git-timesheet",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "pytz>=2021.1",
        "click>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'ggts=git_timesheet.cli:main',
            'git-timesheet=git_timesheet.cli:main',
        ],
    },
    author="Michael McGarrah",
    author_email="mcgarrah@gmail.com",
    description="Generate Git Timesheets from commit history",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mcgarrah/git_timesheet_python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)