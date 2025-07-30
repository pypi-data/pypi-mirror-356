from setuptools import setup, find_packages

setup(
    name="mlpsycho123_sample_package",
    version="0.1.0",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="srinivas",
    author_email="srinivas@example.com",
    url="https://github.com/srinivas/mlpsycho123_sample_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)