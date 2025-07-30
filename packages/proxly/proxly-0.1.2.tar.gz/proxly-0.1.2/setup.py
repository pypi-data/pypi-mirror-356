from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxly",
    version="0.1.2",
    author="Yosefario Dev",
    author_email="github@yosefario.me",
    description="HTTP proxy library for Python using CroxyProxy infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yosefario-dev/freeproxy",
    py_modules=["proxly"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "curl-cffi",
    ],
)
