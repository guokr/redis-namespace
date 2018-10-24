from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='redis_namespace',
    version='0.0.2',
    description='redis namespace',
    url='http://git.fenda.io/usher/redis-namespace',
    install_requires=requirements,
    packages=find_packages(exclude=['tests']),
)
