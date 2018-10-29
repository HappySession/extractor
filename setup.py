import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="happypy",
    version="0.0.1",
    author="Happy Session",
    author_email="happy@happysession.org",
    description="A container to extract NOAA grib data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/happypy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: APACHE 2 License",
        "Operating System :: OS Independent",
    ),
)