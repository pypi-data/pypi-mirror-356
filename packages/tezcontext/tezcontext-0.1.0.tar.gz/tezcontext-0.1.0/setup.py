from setuptools import setup, find_packages

setup(
    name="tezcontext",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"mlpdf": ["data/All_ML_programs.pdf"]},
    description="Access to All ML programs PDF",
    author="Tez",
    # Add other metadata as needed
) 