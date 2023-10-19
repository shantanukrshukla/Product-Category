from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'adding product category'
LONG_DESCRIPTION = 'this service add unique product category into database'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ProductCategory",
    version=VERSION,
    author="shantanu kumar shukla",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    package_data={
        'productcatagory': ['scripts/*.sql', 'resource/*.ini'],
    },
    keywords=['python', 'productcatagory-package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)