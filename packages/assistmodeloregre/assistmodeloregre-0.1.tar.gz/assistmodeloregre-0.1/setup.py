from setuptools import setup, find_packages

setup(
    name="assistmodeloregre",  # debe coincidir con el nombre de la carpeta
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "scikit-learn>=1.3.0",
        "numpy"
    ],
    author="Arnold Sandoval",
    description="Clase personalizada ExtraTrees con confianza",
    python_requires=">=3.8",
)
