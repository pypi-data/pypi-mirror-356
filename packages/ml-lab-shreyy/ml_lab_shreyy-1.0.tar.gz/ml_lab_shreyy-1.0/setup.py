from setuptools import setup, find_packages

setup(
    name='ml_lab_shreyy',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scikit-learn'
    ],
    description='Machine Learning Lab Package with 9 Programs',
    author='Shreyas',
    author_email='ishreyasr@gmail.com',
    license_files = 'MIT',
)
