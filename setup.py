from setuptools import setup, find_packages

setup(
    name='branchconflicts',
    packages=find_packages(include=['requests']),
    version='0.1.0',
    description='Find conflicted files between two branches.',
    author='39matt',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.5'],
    test_suite='tests',
)