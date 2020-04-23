import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unit_converter_roryschadler",
    version="0.1",
    author="Rory Schadler",
    description="Unit converter for NanoMine Knowledge Graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roryschadler/nanomine_unit_converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires'>=3.5.3'
)
