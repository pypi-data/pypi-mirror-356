from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="alfinx_autho",
    version="0.1.4",
    description="HTTP headers auto detection tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maharram Mansimov",
    author_email="maharram@example.com",
    packages=find_packages(),  # <- DƏYİŞDİ
    zip_safe=False
)
