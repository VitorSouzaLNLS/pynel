#!/usr/bin/env python-sirius
"""Setup for install/uninstall Pynel package."""

from setuptools import setup
# import pkg_resources


# def get_abs_path(relative):
#     return pkg_resources.resource_filename(__name__, relative)

version_path = '/pynel/VERSION'

# with open(get_abs_path("README.md"), "r") as _f:
#     _long_description = _f.read().strip()

with open(version_path, "r") as _f:
    __version__ = _f.read().strip()

# with open(get_abs_path("requirements.txt"), "r") as _f:
#     _requirements = _f.read().strip().split("\n")

setup(
    name="pynel",
    version=__version__,
    author="Vitor Souza",
    author_email="vitor.souza@lnls.br",
    description="Button and Base package",
    # long_description=_long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/VitorSouzaLNLS/pynel",
    download_url="https://github.com/VitorSouzaLNLS/pynel",
    license="MIT License",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    packages=["pynel"],
    package_data={'pynel': ['VERSION']},
    # include_package_data=True,
    # install_requires=_requirements,
    # test_suite="tests",
    python_requires=">=3.4",
    zip_safe=False,
)
