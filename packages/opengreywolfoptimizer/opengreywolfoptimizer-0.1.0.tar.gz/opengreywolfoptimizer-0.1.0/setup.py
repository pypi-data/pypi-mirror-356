from setuptools import setup, find_packages

setup(
    name="opengreywolfoptimizer",
    version="0.1.0",
    description="An async-compatible MPI-based Grey Wolf Optimizer",
    author="Vaibhav Goll",
    packages=find_packages(),
    install_requires=["numpy", "mpi4py"],
    python_requires=">=3.7",
)
