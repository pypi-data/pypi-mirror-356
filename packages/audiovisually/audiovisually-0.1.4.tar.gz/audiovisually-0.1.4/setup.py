from setuptools import setup, find_packages

setup(
    name="audiovisually",
    version="0.1.4",
    author="Louie Daans",
    author_email="louiedaans@gmail.com",
    description="A package for audiovisual AI processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "moviepy",
        "googletrans==4.0.2",
        "whisper",
        "torch",
        "nltk",
        "assemblyai",
        "python-dotenv",
        "transformers",
        "tqdm"
    ],
    python_requires=">=3.10",
    project_urls={
        "Documentation": "https://bredauniversityadsai.github.io/2024-25d-fai2-adsai-group-nlp-3/",
        "Source": "https://github.com/BredaUniversityADSAI/2024-25d-fai2-adsai-group-nlp-3/tree/main/audiovisually-pack",
    },
)

# To make wheel and source distribution
# python setup.py sdist bdist_wheel

# To get the package out there for testing (create a testpypi account)
# twine upload -r testpypi dist/*

# Or officially (create a pypi account)
# twine upload dist/*

# Also, check cookiecutter for creating a package from scratch, this can be cleaner.