from setuptools import setup, find_packages

setup(
    name="write_test",
    version="0.1.0",
    author="name",
    description="A package that writes to a personal text file.",
    packages=find_packages(),
    include_package_data=True,
    package_data={"package": ["data.txt"]},
    python_requires=">=3.6",
)

