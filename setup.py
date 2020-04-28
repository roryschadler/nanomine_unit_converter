import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanomine-unit-converter",
    version="0.0.1",
    author="Rory Schadler",
    author_email="rory.h.schadler.21@dartmouth.edu",
    description="Unit converter for NanoMine Knowledge Graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roryschadler/nanomine_unit_converter",
    packages=['nanomine_unit_converter'],
    include_package_data=True,
    install_requires=['pint',
                      'rdflib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2'
)
