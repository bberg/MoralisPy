from setuptools import setup, find_packages

setup(
    name='MoralisPy',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    license='GNU General Public License v3.0',
    description='A python wrapper for the Molaris REST API',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/bberg/MoralisPy',
    author='Ben Berg',
    author_email='1369464+bberg@users.noreply.github.com',
    long_description_content_type='text/markdown'
)