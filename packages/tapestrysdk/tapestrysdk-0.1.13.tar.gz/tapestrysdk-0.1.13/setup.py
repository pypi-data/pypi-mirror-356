from setuptools import setup, find_packages

setup(
    name= "tapestrysdk",
    version="0.1.13",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pymysql",
        "python-dotenv",
        "pycryptodome",
    ],
)