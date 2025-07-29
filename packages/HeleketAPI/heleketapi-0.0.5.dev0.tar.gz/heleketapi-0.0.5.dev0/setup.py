from setuptools import setup, find_packages
from io import open


def read(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


setup(
    name="HeleketAPI",
    version="0.0.5.dev0",
    description="Easy interaction with Heleket API, support for asynchronous approaches",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Fsoky",
    author_email="cyberuest0x12@gmail.com",
    keywords="api heleket asyncio crypto heleketapi",
    license="MIT",
    packages=find_packages()
)
