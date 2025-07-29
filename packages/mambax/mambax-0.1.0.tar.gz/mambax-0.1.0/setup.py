from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mambax",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["torch>=2.0.0", "numpy>=1.21.0"],
    author="Oleg Kufa",
    author_email="os.schischkin@gmail.com",
    description="Optimized Mamba implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jootanehorror/MambaX",
    license="MIT",  
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
