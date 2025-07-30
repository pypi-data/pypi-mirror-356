from setuptools import setup, find_packages

setup(
    name="pqt2_dev_req",
    version="1.0",
    packages=find_packages(),
    include_package_data=False,
    install_requires=["PyQt5"],
)