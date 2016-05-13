import os, sys
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages, Command
from setuptools.command.install_lib import install_lib as _install_lib

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION = '0.9.20'
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
URL = 'https://github.com/voutilad/seal-rookery'
DOWNLOAD_URL = '%s/archive/%s.tar.gz' % (URL, VERSION)

with open('LICENSE.txt') as f:
    LICENSE = f.read()

with open('README.rst') as f:
    README = f.read()


class install_lib(_install_lib):

    def run(self):
        _install_lib.run(self)
        print '==============================================================='
        print ' Remember, run "update-seals" after install to generate seals!'
        print '==============================================================='


class convert(Command):
    description = 'run the image conversion process'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from seal_rookery import convert_images
        convert_images.convert_images()


setup(
    name=NAME,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    package_data={
        'seal_rookery': [
            'seals/*.json',
            'seals/orig/*',
            'www/*.html'
        ]
    },
    version=VERSION,
    description='A collection of court seals that can be used in any project.',
    long_description=README,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    test_suite='test',
    cmdclass={
        'convert': convert,
        'install_lib': install_lib,
    },
    entry_points={
        'console_scripts': [
            'update-seals = seal_rookery.convert_images:convert_images',
        ],
    },
    zip_safe=False,
)
