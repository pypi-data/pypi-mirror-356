# PDF Table and Text Extraction Tool

## Overview
This Python tool extracts tables and text from scanned PDF documents using advanced computer vision and Optical Character Recognition (OCR) techniques. The tool intelligently separates table regions from text content, processes them individually, and combines the results into structured output formats.

## Features
- ✅ **Intelligent Table Detection** - Uses computer vision to identify table structures
- ✅ **OCR Text Extraction** - Extracts text from both tables and regular content
- ✅ **Multiple Output Formats** - Supports CSV, JSON, XLSX, and PDF formats
- ✅ **Command-Line Interface** - Easy-to-use CLI with comprehensive options
- ✅ **Professional Logging** - Detailed logging with file and console output
- ✅ **Error Handling** - Robust error handling and recovery
- ✅ **Configurable Processing** - Adjustable DPI, output paths, and formats

## Installation

### 1. Clone Repository and Install Dependencies
```bash
git clone https://github.com/sathu08/pypdf2extractor.git
cd pdf-table-extractor
pip install -r requirements.txt
```

### 2. Install System Dependencies

#### **Tesseract OCR Configuration**

##### **Windows:**
1. Download and install Tesseract OCR from [official releases](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)
2. Add installation path to system environment variables:
   - Open **System Properties** → **Advanced** → **Environment Variables**
   - Under **System Variables**, find `Path`, click **Edit**, and add:
     ```
     C:\Program Files\Tesseract-OCR
     ```
3. Verify installation:
   ```cmd
   tesseract --version
   ```

##### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng
```

##### **macOS (Homebrew):**
```bash
brew install tesseract
```

#### **Poppler Installation (Required for PDF processing)**

##### **Windows:**
1. Download Poppler from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract and add `bin/` folder to `PATH` environment variable

##### **Linux (Ubuntu/Debian):**
```bash
sudo apt install poppler-utils
```

##### **macOS (Homebrew):**
```bash
brew install poppler
```

### 3. Verify Installation
Test your setup by running:
```bash
python pdf_extractor.py --help
```

## Usage

### Command Line Interface

#### **Basic Usage**
```bash
# Process a PDF with default settings (CSV output)
python pdf_extractor.py document.pdf
```

#### **Advanced Usage**
```bash
# Specify output directory and format
python pdf_extractor.py document.pdf --output ./results --format xlsx

# Custom filename and high DPI
python pdf_extractor.py document.pdf --filename report --dpi 300 --format json

# Verbose logging for debugging
python pdf_extractor.py document.pdf --verbose --output ./debug
```

#### **Complete Options**
```bash
python pdf_extractor.py [PDF_FILE] [OPTIONS]

Options:
  -o, --output DIR          Output directory (default: ./output)
  -f, --filename NAME       Output filename without extension (default: extracted_content)
  --format FORMAT           Output format: csv, json, xlsx, pdf (default: csv)
  --dpi DPI                 DPI for PDF conversion (default: 300)
  -v, --verbose             Enable verbose logging
  -h, --help                Show help message
```

### Programmatic Usage

```python
from pdf_extractor import TableExtractor

# Initialize extractor
extractor = TableExtractor(dpi=300)

# Process PDF and get results
content, saved_file = extractor.process_pdf(
    pdf_path="document.pdf",
    output_path="./results",
    filename="extracted_data",
    file_format="xlsx"
)

# Access extracted content
for page_content in content:
    print(page_content)
```

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **CSV** | Comma-separated values | Data analysis, spreadsheet import |
| **JSON** | JavaScript Object Notation | API integration, web applications |
| **XLSX** | Excel workbook | Business reporting, data presentation |
| **PDF** | Formatted PDF document | Document sharing, archival |

## Project Structure

```
pypdf2extractor/
├── pypdf2extractor.py          # Main extraction script
├── requirements.txt          # Python dependencies
├── README.md                # Documentation
├── log/                  # Default output directory
|   ├── pdf_extractor.log        # Log file (generated)
└── output/                  # Default output directory
    ├── extracted_content.csv
    └── ...
```

## Requirements

### Python Dependencies
```txt
opencv-python>=4.8.0
numpy>=1.24.0
pandas>=2.0.0
pytesseract>=0.3.10
pdf2image>=3.1.0
tabulate>=0.9.0
xhtml2pdf>=0.2.11
```

### System Dependencies
- **Tesseract OCR** - For text recognition
- **Poppler** - For PDF to image conversion
- **Python 3.8+** - Required Python version

## Advanced Features

### Table Detection Algorithm
The tool uses sophisticated computer vision techniques:
1. **Adaptive Thresholding** - Handles varying image quality
2. **Morphological Operations** - Detects table structure lines
3. **Contour Analysis** - Identifies table boundaries
4. **Cell Extraction** - Processes individual table cells

### Error Handling
- **Graceful Degradation** - Continues processing if individual pages fail
- **Detailed Logging** - Comprehensive error tracking and debugging
- **Input Validation** - Validates files and parameters before processing
- **Recovery Mechanisms** - Attempts to recover from common OCR errors

## Troubleshooting

### Common Issues

#### **PDF Conversion Errors**
```bash
Error: PDF conversion failed
```
**Solution:** Ensure Poppler is installed and accessible in PATH

#### **OCR Recognition Issues**
```bash
Error: pytesseract not found
```
**Solution:** 
1. Verify Tesseract installation: `tesseract --version`
2. Check PATH environment variable
3. Reinstall pytesseract: `pip install --upgrade pytesseract`

#### **Table Detection Problems**
- **Low Quality PDFs:** Increase DPI with `--dpi 400`
- **Complex Layouts:** Check logs for detection issues
- **No Tables Found:** Verify PDF contains actual table structures

#### **Memory Issues**
```bash
Error: Out of memory
```
**Solution:** 
- Reduce DPI setting: `--dpi 200`
- Process smaller PDF files
- Increase system RAM allocation

### Debug Mode
Enable verbose logging for detailed troubleshooting:
```bash
python pdf_extractor.py document.pdf --verbose
```

Check log file for detailed error information:
```bash
tail -f pdf_extractor.log
```

## Performance Optimization

### Recommended Settings
- **Standard Documents:** DPI 200-300
- **High-Quality Scans:** DPI 300-400
- **Large Files:** Process in batches
- **Production Use:** Enable logging for monitoring

### Processing Time Guidelines
| PDF Pages | DPI | Estimated Time |
|-----------|-----|----------------|
| 1-10      | 300 | 30-60 seconds  |
| 11-50     | 300 | 2-5 minutes    |
| 50+       | 200 | 5+ minutes     |

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for detailed error information
3. Open an issue on GitHub with:
   - Error messages
   - Sample PDF (if possible)
   - System information
   - Log file contents
