from setuptools import setup, find_packages

setup(
    name="my_hacklib",
    version="0.1.0",
    author="Wada Kaede",
    description="A Python library for various networking and cryptographic functions.",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "scapy",
        "paramiko"
    ],
    python_requires=">=3.6",
)