# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in amasi/__init__.py
from amasi import __version__ as version

setup(
	name='amasi',
	version=version,
	description='Stock Item Customizations',
	author='Greycube',
	author_email='admin@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
