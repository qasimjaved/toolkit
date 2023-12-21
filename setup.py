from setuptools import find_packages, setup


setup(
    name='toolkit',  # Name of your package
    version='0.1',  # Package version
    author='Qasim Javed',  # Your name or the name of the package author
    author_email='qasim.javed012@gmail.com',  # Author's email
    description='WebScraping Helpers Package',  # A short description
    long_description=open('README.md').read(),  # Long description read from the README.md
    long_description_content_type='text/markdown',  # Specifies the format of the long description
    url='https://github.com/qasimjaved/helpers',  # Link to the repository
    packages=find_packages(),  # Finds and lists all packages
    install_requires=[
        'Scrapy',  # Example of a dependency, add others as needed
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Minimum version requirement of the package
)