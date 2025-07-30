from setuptools import setup, find_packages

setup(
    name="wehaveatogether",
    version="0.1.1",
    author="wehaveatogether",
    description="Short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
