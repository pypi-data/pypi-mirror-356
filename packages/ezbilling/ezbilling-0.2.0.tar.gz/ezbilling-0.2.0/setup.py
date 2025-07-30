from setuptools import setup, find_packages

setup(
    name="ezbilling",           # Must be unique on PyPI
    version="0.2.0",
    author="Nithesh",
    author_email="nithish@dreaminfinity.com",
    description="Make payment gatway integration easy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ezbillpay",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
