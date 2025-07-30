from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='bloom_cascade',
    version='1.0.2',
    packages=find_packages(),
    install_requires=['rbloom==1.5.2'],
    long_description=description,
    long_description_content_type='text/markdown'
)