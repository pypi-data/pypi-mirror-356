from setuptools import setup, find_packages
import os

# Intentar leer README.md
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Datos de prueba SENEPA"

setup(
    name="cliente-dato-publico",
    version="0.1.0",
    description="Datos de prueba SENEPA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Christian Gamon",
    author_email="Christian.gamon@fpuna.edu.py",
    url="https://github.com/cgamon/cliente_dato_publico.git",
    packages=find_packages(),
    install_requires=[
        "requests",
        "simplekml"
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'cliente-dato = cliente_dato_publico.main:menu'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
)
