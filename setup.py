import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

VERSION = '0.9.3'
AUTHOR = 'Mike Lissner'
EMAIL = 'info@free.law'
NAME = 'seal_rookery'
KEYWORDS = ["legal"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
URL = 'https://github.com/freelawproject/seal-rookery'

with open('LICENSE.txt') as f:
    LICENSE = f.read()

with open('README.rst') as f:
    README = f.read()

setup(
    name=NAME,
    packages=find_packages(exclude=('tests',)),
    version=VERSION,
    description='A collection of court seals that can be used in any project.',
    long_description=README,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    license=LICENSE,
    url=URL,
    download_url='%s/archive/%s.tar.gz' % (URL, VERSION),
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    test_suite='test',
)
