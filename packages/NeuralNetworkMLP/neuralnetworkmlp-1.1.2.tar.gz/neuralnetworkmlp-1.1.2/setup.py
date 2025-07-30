from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description_md = fh.read()

setup(
    name="NeuralNetworkMLP",
    version="1.1.2",
    author="Panagiotis Trypos",
    author_email="panagiotis.trypos23@gmail.com",
    description="A class that implements an MLP neural network",
    long_description=long_description_md,
    long_description_content_type="text/markdown",
    url="https://github.com/ThePhantom2307/MLP-Neural-Network",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)