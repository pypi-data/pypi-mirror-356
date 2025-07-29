from setuptools import setup, find_packages


setup(
    name='caf-analysis',
    version='1.40',
    author='Archie Baldock',
    description='TOF peak finding for CaF data analysis',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)