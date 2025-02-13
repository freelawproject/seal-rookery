import os

from setuptools import find_packages, setup

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION = "2.3.1"
AUTHOR = "Free Law Project"
EMAIL = "info@free.law"
NAME = "seal_rookery"
KEYWORDS = ["legal", "seals"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
URL = "https://github.com/freelawproject/seal-rookery"
DOWNLOAD_URL = "%s/archive/%s.tar.gz" % (URL, VERSION)

with open("README.md", encoding="utf-8") as f:
    README = f.read()


setup(
    name=NAME,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    package_data={"seal_rookery": ["seals/*.json"]},
    version=VERSION,
    description="A collection of court seals that can be used in any project.",
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    test_suite="test",
    zip_safe=False,
)
