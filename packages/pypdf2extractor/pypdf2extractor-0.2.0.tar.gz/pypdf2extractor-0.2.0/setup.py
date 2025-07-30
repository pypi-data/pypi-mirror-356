from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pypdf2extractor",
    version="0.2.0",
    author="SathyaPrakash",
    author_email="sathiyaprakash881@gmail.com",
    description="A tool to extract text and tables from PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sathu08/pypdf2extractor",
    license="MIT",  
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "pandas",
        "pytesseract",
        "pdf2image",
        "tabulate",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "pypdf2extractor=pypdf2extractor.extractor:main", 
        ],
    },
)
