from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pyro-lang",
    version="0.1.0",
    author="Pyro Contributors",
    description="A friendlier Python that compiles to Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyro-lang/pyro",
    project_urls={
        "Bug Reports": "https://github.com/pyro-lang/pyro/issues",
        "Source": "https://github.com/pyro-lang/pyro",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "pyro = pyro.cli:main",
        ],
    },
    include_package_data=True,
)
