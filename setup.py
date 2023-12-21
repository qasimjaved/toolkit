from setuptools import find_packages, setup

setup(
    name="helpers",
    packages=find_packages(include=["helpers", "helpers.*"]),
    description="WebScraping Helpers Package",
    version="0.1",
    url="https://github.com/qasimjaved/helpers",
    author="qasim_javed",
    author_email="qasim.javed012@gmail.com",
    keywords=["pip", "helpers"],
    install_requires=["Scrapy"],
)
