from setuptools import setup, find_packages

setup(
    name="GraphePython",
    version="1.4",
    author="Saubion Sami",
    author_email="sami.saubion@gmail.com",
    description="Implementation of Dijkstra's algorithm with graph visualization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SAMSAM55yt/GraphePython",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.0",
        "networkx>=2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)