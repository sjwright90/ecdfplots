from setuptools import setup, find_packages

setup(
    author="Samuel JS Wright",
    description="Small package for plotting empirical cumulative distribution functions (ECDFs)",
    name="ecdfplots",
    version="0.1.0",
    packages=find_packages(include=["ecdfplots", "ecdfplots.*"]),
    install_requires=[
        "numpy>=1.22",
        "pandas>=1.5",
        "matplotlib>=3.7",
        "statsmodels>=0.13",
    ],
    python_requires=">=3.9",
)
