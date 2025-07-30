from setuptools import setup, find_packages

setup(
    name="demoExTest",
    version="1.0",
    packages=find_packages(),  # Важно! Найдёт demoExTest, demoExTest.database, demoExTest.ui
    include_package_data=True,
    install_requires=["PyQt5"],
)