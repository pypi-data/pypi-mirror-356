from setuptools import setup, find_packages

setup(
    name="tnncli",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",

    description="",

    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)