from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='redis_namespace',
    version='0.0.4',
    description='redis namespace',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/guokr/redis-namespace',
    author='zrq495',
    author_email='zrq495@gmail.com',
    keywords=['redis namespace', 'redis prefix'],
    license='MIT',
    install_requires=requirements,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
