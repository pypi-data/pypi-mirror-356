from setuptools import setup, find_packages

setup(
    name="sms_gateway_sdk",
    version="0.1.0",
    description="Python SDK for interacting with a FastAPI-based SMS gateway using ESP32 and GSM module.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Islam Remache",
    author_email="myname@esi.dz",
    url="https://github.com/tonusername/sms_gateway_sdk",  
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
