from setuptools import setup, find_packages

setup(
    name="pysick",
    version="14.8.8",
    packages= ['pysick'],
    package_data={'pysick':['assets/*.ico'],'pysick':['assets/*.png']},
    install_requires=[],
    author="CowziiK",
    author_email="cowziik@email.com",
    description="A lightweight 2D game framework using Tkinter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/COWZIIK/pysick",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
