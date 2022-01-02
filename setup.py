from setuptools import setup, find_packages

setup(
    name='MoralisPy',
    version='1.0.1',
    packages=find_packages(exclude=['tests*']),
    license='GNU General Public License v3.0',
    description='A python wrapper for the Molaris REST API',
    long_description=open('README.md').read(),
    install_requires=[
        'requests',
    ],
    url='https://github.com/bberg/MoralisPy',
    author='Ben Berg',
    author_email='benberg00@gmail.com',
    long_description_content_type='text/markdown'
)