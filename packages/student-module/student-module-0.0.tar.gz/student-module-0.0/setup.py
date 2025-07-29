from setuptools import setup, find_packages

setup(
    name="student-module",
    version="0.0",
    packages=find_packages(),
    description="Student class with get_details, txtFile, db, and excel methods for storing data",
    author="Renuka",
    author_email="renuka26092001@gmail.com",
    python_requires='>=3.6',
    install_requires=[
        "openpyxl",
        "mysql-connector-python"
    ],
)
