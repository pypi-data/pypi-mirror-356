import setuptools

setuptools.setup(
    name = "mr_z3r0_calculator",
    version = "0.2.0",
    author = "author",
    author_email = "saranraja@kissflow.com",
    description = "This is simple calculator app",
    long_description = "This is simple calculator app",
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6"
)