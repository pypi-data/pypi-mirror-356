# setup.py

from setuptools import setup, find_packages

setup(
    name="abarna_calc07",  # ✅ This is the PyPI name (hyphens allowed)
    version="0.1.2",     # 🔁 Change this for every new upload
    author="Abarna",
    author_email="abarnamagesh1707@gmail.com",
    description="A simple calculator package by Abarna",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/meow074",  # Optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your chosen license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
