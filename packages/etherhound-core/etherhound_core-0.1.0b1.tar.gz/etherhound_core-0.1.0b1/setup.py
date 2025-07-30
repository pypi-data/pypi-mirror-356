from setuptools import setup, find_packages

setup(
    name="etherhound-core",
    version="0.1.0b1",
    description="EtherHound Core - Blockchain Event Scanner Server",
    long_description=open("readme.md", "r+").read(),
    author="SpicyPenguin",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "fastapi[standard]",
        "python-dotenv",
        "web3",
        "pydantic",
        "typer"
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "hound=houndcore.cli.__main__:app"
        ],
    },
)