import os, sys
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

VERSION = '0.9.1'
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


def _post_install(dir):
    from subprocess import call
    print 'calling here: ' + os.path.join(dir, NAME)
    call([sys.executable, '_post_install.py', DOWNLOAD_URL],
         cwd=os.path.join(dir, NAME))


class install(_install):
    """
    See http://stackoverflow.com/questions/250038/how-can-i-add-post-install-\
        scripts-to-easy-install-setuptools-distutils for more details.
    """
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg='Executing _post_install.py task')

setup(
    name=NAME,
    packages=find_packages(exclude=('tests',)),
    install_requires=['requests'],
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
    include_package_data=True,
    test_suite='test',
    cmdclass={'install': install},
    zip_ok=False,
    zip_safe=False,
)
