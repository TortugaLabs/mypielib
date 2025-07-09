from setuptools import setup, find_packages
from mypielib.version import VERSION

setup(
    name="mypielib",
    version=VERSION,
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
