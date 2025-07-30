from setuptools import setup, find_packages

setup(
    name="ezbilling",           # Must be unique on PyPI
    version="0.5.0",
    author="Nithesh",
    author_email="nithish@dreaminfinity.com",
    description="Make payment gatway integration easy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ezbillpay",
    packages=find_packages(),
    install_requires=[
        'requests'  # This ensures requests is installed
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependencies = ["requests>=2.25.1"],
    python_requires=">=3.7",
)
