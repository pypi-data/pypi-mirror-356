from setuptools import setup, find_packages

setup(
    name="am_calculator",
    version="0.1.0",
    author="amit",
    author_email="amitkm644@gmail.com",
    description="A simple calculator package",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "calculator=calculator.calculator:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)