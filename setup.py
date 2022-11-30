from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(name="snowball-fight", install_requires=requirements, packages=find_packages(), include_package_data=True)
