import re
from codecs import open
from os import path
from typing import List

import pkg_resources
from setuptools import find_packages, setup


def read(name: str) -> str:
    repo_root = path.abspath(path.dirname(__file__))
    with open(path.join(repo_root, name)) as f:
        return f.read()


def read_requirements(name: str) -> List[str]:
    return [str(r) for r in pkg_resources.parse_requirements(read(name))]


def get_version() -> str:
    version_file = "_version.py"
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", read(version_file), re.M)
    assert match is not None, f"Unable to find version string in {version_file}"
    return match.group(1)

setup(
    version=get_version(),
    name="chalk-harness",
    author="Chalk AI, Inc.",
    description="Python wrapper for Chalk's CLI",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires=">=3.8.0",
    url="https://chalk.ai",
    packages=find_packages(exclude=("tests",)),
    install_requires=read_requirements("requirements.txt"),
    include_package_data=True,
    package_data={"chalkharness": ["py.typed"]},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    setup_requires=[
        "setuptools_scm",
    ],
)
