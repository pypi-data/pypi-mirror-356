from setuptools import setup, find_packages

setup(
    name="pqt_dev_req",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["PyQt5"],
)