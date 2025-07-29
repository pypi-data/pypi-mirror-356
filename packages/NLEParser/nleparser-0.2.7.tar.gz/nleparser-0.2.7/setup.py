from setuptools import setup, find_packages

setup(
    name="NLEParser",
    version="0.2.7",
    author="NatanLang",
    author_email="natanrcorreiatr@gmail.com",
    description="A Natural Language processing parser for Zork-style games",
    
    # Boa prática: especificar o encoding para evitar erros em diferentes sistemas
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",

    # 1. Diz ao setuptools que a raiz dos pacotes (indicada por '') está na pasta 'src'
    package_dir={"": "src"},
    
    # 2. Encontra automaticamente todos os pacotes dentro da pasta 'src'
    packages=find_packages(where="src"),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # Nota: Python 3.13 é muito recente. Se seu código for compatível com versões
    # anteriores (ex: 3.8+), usar ">=3.8" pode aumentar o alcance do seu pacote.
    python_requires=">=3.13",
)