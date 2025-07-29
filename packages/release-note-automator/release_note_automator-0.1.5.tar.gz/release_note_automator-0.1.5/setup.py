from setuptools import setup, find_packages, os

setup(
    name="release-note-automator",
    version="0.1.5",
    author="Ankur Helak",
    author_email="ankurhelak@gmail.com",
    description="A CLI tool to automate fetching, cleaning, summarizing, and posting release notes from Azure DevOps.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/ankur-helak/release-note-automator",
    project_urls={
        "Bug Tracker": "https://github.com/ankur-helak/release-note-automator/issues",
    },
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "questionary",
        "wcwidth",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "rlauto=rlauto.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
)
