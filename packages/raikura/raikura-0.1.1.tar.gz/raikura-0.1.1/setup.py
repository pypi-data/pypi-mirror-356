from setuptools import setup, find_packages
import pathlib

# Set the base directory
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Load the long description from README.md
long_description = (BASE_DIR / "README.md").read_text(encoding="utf-8")

# Load dependencies from requirements.txt
requirements = (BASE_DIR / "requirements.txt").read_text(encoding="utf-8").splitlines()

setup(
    # Package metadata
    name="raikura",  # The name of your package
    version="0.1.1",  # Follow semantic versioning: MAJOR.MINOR.PATCH
    description="Advanced AI/ML library that enhances scikit-learn with DL, NLP, AutoML, fairness, and interpretability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Naitik Gupta",
    author_email="hylendust@gmail.com",
    url="https://github.com/orgs/RaykenAI/raikura",
    license="MIT",

    # Package structure
    packages=find_packages(),  # Automatically finds all sub-packages like raikura.core
    include_package_data=True,  # Include files from MANIFEST.in
    python_requires=">=3.8",

    # Runtime dependencies
    install_requires=requirements,

    # Optional metadata for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],

    # Project-level URLs
    project_urls={
        "Documentation": "https://github.com/orgs/RaykenAI/raikura#readme",
        "Source": "https://github.com/orgs/RaykenAI/raikura",
        "Bug Tracker": "https://github.com/orgs/RaykenAI/raikura/issues",
    }
)
