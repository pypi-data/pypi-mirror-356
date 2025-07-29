from setuptools import setup
import pathlib

cwd = pathlib.Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="portalsmp",
    version="1.1",
    author="bleach",
    author_email="year0001@internet.ru",
    description="A Python Module for interacting with Portals Marketplace API",
    url="https://github.com/bleach-hub/portalsmp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["portalsmp"],
    install_requires=[
    "pyrogram>=2.0.106",
    "tgcrypto>=1.2.5",
    "curl_cffi>=0.10.0",
    "pycryptodome>=3.21.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)