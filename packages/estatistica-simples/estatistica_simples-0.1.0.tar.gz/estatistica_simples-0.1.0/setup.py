# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='estatistica_simples',
    version='0.1.0',
    author='Rodrigo Rocha',
    author_email='vadan.2r@gmail.com',
    description='Um pacote Python simples para cálculos estatísticos básicos.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vadan2r/estatistica_simples', 
    packages=find_packages(),  # Encontra automaticamente os pacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
