#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from jenskipper import __version__


HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()
NEWS = open(os.path.join(HERE, 'NEWS.txt')).read()


setup(
    name='jenskipper',
    version=__version__,
    description="",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Luper Rouch',
    author_email='luper.rouch@gmail.com',
    url='',
    license='Apache Software License 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts':
            ['jenskipper=jenskipper.cli:main']
    }
)
