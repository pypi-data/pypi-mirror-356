from setuptools import setup, find_packages

setup(
    name="lambdakit-response",
    version="1.0.2",
    description="Lightweight response utility for AWS Lambda proxy integration",
    author="mtrshuvo",
    author_email="mtrshuvo@gmail.com",
    packages=find_packages(),
    install_requires=[
        "orjson>=3.9.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
