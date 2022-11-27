import re

from setuptools import setup


with open("README.rst") as f:
    readme = f.read()


with open("click_help_colors/__init__.py") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)


setup(
    name="click-help-colors",
    version=version,
    packages=["click_help_colors"],
    description="Colorization of help messages in Click",
    long_description=readme,
    url="https://github.com/click-contrib/click-help-colors",
    keywords=["click"],
    license="MIT",
    install_requires=["click>=7.0,<9"],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
)
