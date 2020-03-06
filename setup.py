import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openx-json-grzracz",
    version="0.0.1",
    author="Grzegorz Raczek",
    author_email="grz.raczek@gmail.com",
    description="Small program for JSON operations made for OpenX Python internship test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grzracz/OpenX-JSON",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
