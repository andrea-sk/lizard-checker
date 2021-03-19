from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="lizard-checker",
    version="0.1",
    description="Check avro DIF ouput in a declarative way",
    long_description=readme(),
    author="Andrea Dodet",
    author_email="andrea.dodet@mail-bip.com",
    install_requires=["fastavro"],
    packages=find_packages("src"),
    entry_points={"console_scripts": ["dif-checker=src.checker_cli:main"]},
)
