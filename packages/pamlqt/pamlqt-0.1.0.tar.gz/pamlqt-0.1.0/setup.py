from setuptools import setup, find_packages

setup(
    name="pamlqt",
    version="0.1.0",
    author="qinti",
    author_email="qinti@zju.edu.cn",
    description="A toolkit for phylogenetic analysis with codeml",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qinti2023/pamlqt",
    include_package_data=True,
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "biopython>=1.78",
        "ete3>=3.1.2"
    ],
    entry_points={
        "console_scripts": [
            "pamlqt=pamlqt.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
