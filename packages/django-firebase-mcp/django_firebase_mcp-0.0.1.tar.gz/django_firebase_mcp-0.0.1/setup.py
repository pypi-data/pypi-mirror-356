import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-firebase-mcp",                      # This is the name of the package
    version="0.0.1",                                 # The initial release version
    author="Raghvendra Dasila",                      # Full name of the author
    description="A comprehensive Django app that implements Firebase Model Context Protocol (MCP) server, enabling AI agents to interact with Firebase services seamlessly through structured tools and interfaces.",
    long_description=long_description,               # Long description read from the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='django-firebase-mcp'),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                              # Information to filter the project on PyPi website
    python_requires='>=3.10',                       # Minimum version requirement of the package
    py_modules=["django-firebase-mcp"],              # Name of the python package
    package_dir={'': 'django-firebase-mcp'},         # Directory of the source code of the package
    install_requires=[]                              # Install other dependencies if any
)