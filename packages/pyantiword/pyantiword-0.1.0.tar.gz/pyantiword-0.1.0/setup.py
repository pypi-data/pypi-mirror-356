from setuptools import setup, find_packages

setup(
    name="pyantiword",
    version="0.1.0",
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
)
