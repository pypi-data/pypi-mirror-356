from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    Name="fleetingviews",
    Version="0.2",
    author="Bruno Arellano",
    author_email="arellanobruno@hotmail.com",
    description="Facilitates view creation and management in Flet applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArellanoBrunoc/FleetingViews",
    project_urls={
        "Bug Tracker": "https://github.com/ArellanoBrunoc/FleetingViews/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["flet"],
    include_package_data=True,
    python_requires=">=3.7",
)
