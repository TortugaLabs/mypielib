from setuptools import setup, find_packages
from mypielib.version import VERSION,ERROR_STR

setup(
    name="mypielib",
    version=None if VERSION == ERROR_STR else VERSION,
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your library needs here
    ],
    author="Alejandro Liu",
    author_email="alejandro_liu@hotmail.com",
    description="A simple Python library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TortugaLabs/mypielib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
