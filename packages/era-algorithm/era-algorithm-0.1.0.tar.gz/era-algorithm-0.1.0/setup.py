from setuptools import setup, find_packages

setup(
    name='era-algorithm',
    version='0.1.0',
    description='Eigensystem Realization Algorithm (ERA) functions for system identification',
    author='Theodore Li',
    author_email='theodoreli927@gmail.com',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
    'numpy',
    'scipy',
],
    license='MIT',
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],

)

