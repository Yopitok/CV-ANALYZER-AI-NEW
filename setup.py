# File: setup.py
from setuptools import setup, find_packages

setup(
    name='cv_analyzer_src',
    version='1.0.0',
    author='Yopit',
    description='A Streamlit CV Analyzer application',
    packages=find_packages(),
    python_requires='>=3.8',
)