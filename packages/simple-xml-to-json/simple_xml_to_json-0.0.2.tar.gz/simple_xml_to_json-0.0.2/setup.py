from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="simple-xml-to-json",
    version="0.0.2",
    install_requires = [
        'lxml',
    ],
    description="A simple xml to json converter",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["simple_xml_to_json"],
    author="Christopher Abanilla",
    license="MIT"
)
