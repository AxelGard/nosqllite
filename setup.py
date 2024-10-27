from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nosqllite",
    version="0.1.0",
    description="A simple nosql data base",
    url="https://github.com/AxelGard/nosqllite",
    author="Axel Gard",
    author_email="axel.gard@tutanota.com",
    license="MIT",
    packages=["nosqllite"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            "black",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
