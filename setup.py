from setuptools import setup, find_packages

setup(
    name='branchconflicts',
    packages=find_packages(include=['requests']),
    version='0.1.0',
    description='Find conflicted files between two branches.',
    author='39matt',
)