#!env/bin/python
from setuptools import setup

setup(
    name="pymailcheck",
    version="1.0.0rc1",
    description="Suggest corrections to user-misspelled email addresses",
    url="https://github.com/dbarlett/pymailcheck",
    author="Dylan Barlett",
    author_email="dylan.barlett@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
    ],
    keywords="email mailcheck",
    packages=["pymailcheck"],
    install_requires=open("requirements.txt").readlines()
)
