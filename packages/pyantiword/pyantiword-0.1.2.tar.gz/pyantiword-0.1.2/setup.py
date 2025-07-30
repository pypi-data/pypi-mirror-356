from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pyantiword",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pyantiword": [
            "antiword",
            "antiword_share/*",
        ],
    },
    install_requires=[],
    author="Vitor Hugo Moreira Reis",
    description="Python wrapper for antiword with bundled binary and data files",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
