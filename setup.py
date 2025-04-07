from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='branchconflicts',
    packages=find_packages(),
    version='0.1.6',
    description='Find conflicted files between two branches.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='39matt',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.5'],
    test_suite='tests',
)