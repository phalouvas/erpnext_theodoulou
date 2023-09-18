from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in theodoulou/__init__.py
from theodoulou import __version__ as version

setup(
	name="theodoulou",
	version=version,
	description="Customizations of theodoulouparts.com",
	author="KAINOTOMO PH LTD",
	author_email="info@kainotomo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
