from setuptools import setup, find_packages

setup(
    name="pyverif",
    version="0.1.1",
    author="Ninmegne Paul",
    author_email="paul02prof@gmail.com",
    description="Package de vérification",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/paul02prof/pyverif",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        # liste des dépendances
    ],
)