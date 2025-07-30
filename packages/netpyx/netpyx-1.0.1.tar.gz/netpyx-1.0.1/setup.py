from setuptools import setup, find_packages

setup(
    name="netpyx",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="José Luis (Pepe)",
    author_email="jlci811122@gmail.com",
    description="A simple HTTP client wrapper for requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
