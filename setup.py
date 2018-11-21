import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('redis_namespace/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='redis_namespace',
    version=version,
    description='namespaced subset of your redis keyspace',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/guokr/redis-namespace',
    author='zrq495',
    author_email='zrq495@gmail.com',
    keywords=['redis namespace', 'redis prefix'],
    license='MIT',
    install_requires=requirements,
    packages=find_packages(exclude=['tests']),
    tests_require=[
        'mock',
        'pytest',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
