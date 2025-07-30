from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='epgm_model',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'pandas',
        'matplotlib',
        'scipy'
    ],
    author='Haris Masood',
    author_email='haris_masood@yahoo.com',
    description='Implementation of the EPGM model for time series forecasting.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial',
    ],
)
