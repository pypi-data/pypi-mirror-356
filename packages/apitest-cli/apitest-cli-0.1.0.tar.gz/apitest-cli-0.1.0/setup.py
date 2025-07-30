from setuptools import setup, find_packages

setup(
    name="apitest-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "requests>=2.25",
        "rich>=12.0",
        "textblob>=0.15",
    ],
    entry_points={
        "console_scripts": [
            "apitest=apitest:cli",
        ],
    },
    author="Hamza Ferrahoglu",
    author_email="hamzacferrahoglu@gmail.com",
    description="A CLI tool for testing HTTP APIs with request saving, templates, and sentiment analysis.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HFerrahoglu/apitest-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)