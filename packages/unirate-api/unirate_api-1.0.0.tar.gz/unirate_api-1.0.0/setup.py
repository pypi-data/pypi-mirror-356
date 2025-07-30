from setuptools import setup, find_packages

setup(
    name="unirate-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Unirate Team",
    author_email="admin@unirateapi.com",
    description="Official Python client for the Unirate API - real-time and historical currency exchange rates, plus VAT rates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UniRate-API/unirate-api-python",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
) 