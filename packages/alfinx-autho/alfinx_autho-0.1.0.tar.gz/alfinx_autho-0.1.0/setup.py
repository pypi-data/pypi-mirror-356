from setuptools import setup, find_packages

setup(
    name="alfinx_autho",
    version="0.1.0",
    author="Maharram Mansimli",
    author_email="mnismlim@gmail.com",
    description="Headers auto-detection library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
