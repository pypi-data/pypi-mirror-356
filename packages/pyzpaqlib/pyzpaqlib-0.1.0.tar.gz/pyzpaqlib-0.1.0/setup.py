from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyzpaqlib',
    version='0.1.0',
    author='SamyLabs',
    author_email='help.samylabs@gmail.com',
    description='A modern and easy-to-use Python wrapper for the ZPAQ archiver.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ahhgo326/pyzpaqlib',
    packages=find_packages(exclude=['source', 'source.*']),
    package_data={
        'pyzpaqlib': ['bin/zpaq.exe', 'bin/zpaq64.exe'],
    },
    license='MIT',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Archiving :: Compression',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
