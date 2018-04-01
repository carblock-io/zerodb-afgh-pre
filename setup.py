from setuptools import setup, find_packages
from os.path import dirname, abspath, join

INSTALL_REQUIRES = [
    'JPype1',
    'cachetools',
    'zerodb',
    ]

setup(
    name="zerodb.afgh",
    version="0.10",
    description="AFGH proxy re-encryption for ZeroDB",
    author="ZeroDB Inc.",
    author_email="michael@zerodb.io",
    license="Proprietary",
    url="https://github.com/carblock-io/zerodb-afgh-pre",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    # package_dir={"": "src"},
    include_package_data=True,
    namespace_packages=['zerodb'],
)
