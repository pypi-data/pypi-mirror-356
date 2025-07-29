# setup.py
# This file is used to configure your library for packaging and distribution.
from setuptools import setup, find_packages

# FIX: Specify encoding='utf-8' to prevent UnicodeDecodeError on Windows.
setup(
    name='tipe_sim',
    version='1.2.1', # Version bump for the bug fix
    packages=find_packages(),
    author='Aadidil ilyas',
    author_email='',
    description='A Python library to generate professional TIPE simulations using the Gemini API.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tipe_sim',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
