"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.7
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""
from setuptools import setup, find_packages
import re

def get_version():
    with open("spec2chat/version.py", "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*"(.+)"', content)
    if match:
        return match.group(1)
    raise RuntimeError("No version found in version.py")

setup(
    name="spec2chat",
    version=get_version(),
    author="María Jesús Rodríguez Sánchez",
    author_email="mjesusrodriguez@ugr.es",
    description="A Python library for generating task-oriented dialogue systems from service specifications (PPTalk).",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mjesusrodriguez/spec2chat",  # Replace with your real GitHub URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai>=0.27.0",
        "pymongo>=4.0.0,<5.0.0",
        "spacy==3.7.2",
        "nltk>=3.7",
        "python-dotenv>=0.21.0",
        "dnspython",
        "setuptools>=65.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    license="Apache-2.0",
    python_requires='>=3.8',
)