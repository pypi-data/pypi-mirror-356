from setuptools import setup, find_packages

setup(
    name='qmetro',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'numpy>=1.26.4',
        'scipy>=1.14.1',
        'cvxpy>=1.6.0',
        'matplotlib>=3.10.0',
        'networkx>=3.3',
    ]
)
