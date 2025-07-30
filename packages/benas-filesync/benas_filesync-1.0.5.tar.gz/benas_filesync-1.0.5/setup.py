'''
@description: Setup script for the filesync package.
'''

from setuptools import setup, find_packages

setup(
    name='benas_filesync',
    version='1.0.5',
    description='File synchronization script with backup and versioning',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Benas Untulis',
    author_email="untulisb@gmail.com",
    url="https://github.com/BUntulis/filesync", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'filesync = benas_filesync.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        # If there are any dependencies, list them here
    ],
)
