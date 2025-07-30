To make your `README.md` display correctly on **PyPI**, it must:

1. Use valid **Markdown syntax** only (no reStructuredText).
2. Avoid GitHub-style emojis (`✅`) which may not render correctly on PyPI.
3. Reference **valid links** (PyPI doesn’t support `javascript:` or broken URLs).
4. Be UTF-8 encoded and declared properly in `setup.py`.

---

### ✅ Cleaned & PyPI-Ready Version (Key Edits Only)

Here's an **updated version of your `README.md`**, cleaned and styled for PyPI compatibility:

---

````markdown
# PDF Table and Text Extraction Tool

## Overview
This Python tool extracts tables and text from scanned PDF documents using advanced computer vision and Optical Character Recognition (OCR) techniques. It separates table regions from text, processes them individually, and outputs structured results.

## Features
- Intelligent Table Detection using OpenCV
- OCR-based Text Extraction (via Tesseract)
- Supports output formats: CSV, JSON, XLSX, and PDF
- Easy-to-use Command-Line Interface (CLI)
- Logging to file and console
- Error Handling and Input Validation
- Configurable DPI, output format, and file naming

## Installation

Install from PyPI:

```bash
pip install pypdf2extractor
````

Or clone the repo:

```bash
git clone https://github.com/sathu08/pypdf2extractor.git
cd pypdf2extractor
pip install .
```

### System Dependencies

#### Tesseract OCR

**Windows**
Download from: [Tesseract releases](https://github.com/tesseract-ocr/tesseract/releases)
Add install folder to system `PATH`.

**Linux**

```bash
sudo apt install tesseract-ocr
```

**macOS**

```bash
brew install tesseract
```

#### Poppler

**Windows**
Download from: [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
Add `bin/` to `PATH`.

**Linux**

```bash
sudo apt install poppler-utils
```

**macOS**

```bash
brew install poppler
```

## CLI Usage

### Basic

```bash
pypdf2extractor input.pdf
```

### Advanced

```bash
pypdf2extractor input.pdf --output results --format xlsx --dpi 300
```

### All Options

```bash
pypdf2extractor [PDF_FILE] [OPTIONS]

Options:
  -o, --output DIR         Output directory
  -f, --filename NAME      Output filename (no extension)
  --format FORMAT          csv, json, xlsx, pdf
  --dpi DPI                PDF resolution (default: 300)
  -v, --verbose            Verbose logging
  -h, --help               Show help
```

## Programmatic Usage

```python
from pypdf2extractor import extractor

extractor.main()
```

## Output Formats

| Format | Description            |
| ------ | ---------------------- |
| CSV    | Spreadsheet compatible |
| JSON   | For APIs/web           |
| XLSX   | For reporting          |
| PDF    | Final formatted file   |

## Requirements

**Python 3.10+**

**Python Packages**
See `requirements.txt`, including:

* opencv-python
* numpy
* pandas
* pytesseract
* pdf2image
* tabulate
* xhtml2pdf

**System Tools**

* Tesseract OCR
* Poppler

## Troubleshooting

### Tesseract not found

Make sure it's installed and available in PATH:

```bash
tesseract --version
```

### Poppler errors

Ensure `pdftoppm` is in your system's `PATH`.

### Performance Tips

* Use `--dpi 200` for faster results
* Use `--verbose` to see logs

## License

MIT License

## Support

Please raise issues on the [GitHub repository](https://github.com/sathu08/pypdf2extractor/issues).

```
```
