# Import required functions
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Call setup function
setup(
    author="Josue Afouda",
    description="A package for converting impyrial lengths and weights.",
    name="cr_package_installable",
    version="0.1.2",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy>=1.10',
        'pandas'
    ]
)