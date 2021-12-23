from setuptools import setup, find_packages

setup(
    name='MoralisPy',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='none',
    description='A wrapper for the Molaris REST API https://deep-index.moralis.io/api-docs/#/',
    long_description=open('README.md').read(),
    install_requires=[],
    url='REPOSITORY_URL',
    author='Ben Berg',
    author_email='benberg00@gmail.com'
)