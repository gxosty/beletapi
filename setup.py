from setuptools import setup

setup(
    name="beletapi",
    version="0.1.0",
    description="Belet REST API client",
    author="gxost",
    author_email="6321b5arsi@gmail.com",
    packages=[
        "beletapi/",
        "beletapi/downloaders",
        "beletapi/models",
    ],
    install_requires=[],
)
