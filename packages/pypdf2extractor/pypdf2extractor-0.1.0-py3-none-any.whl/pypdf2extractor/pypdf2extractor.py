#!/usr/bin/env python3
"""
PDF Table and Text Extraction Tool

A Python script for extracting tables and text from scanned PDF documents
using computer vision and OCR techniques.

Author: [Your Name]
Version: 2.0.0
Date: 2025-06-19

Dependencies:
    - opencv-python
    - numpy
    - pandas
    - pytesseract
    - pdf2image
    - tabulate
    - xhtml2pdf

Usage:
    python pdf_extractor.py input.pdf --output ./results --format csv --tosave
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
from tabulate import tabulate

# Configure logging
def logging_setup(logger_name: str, logger_filename: str, log_folder: str = "log"):
    os.makedirs(log_folder, exist_ok=True)
    log_path = os.path.join(log_folder, logger_filename)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger


logger = logging_setup("pdf_extractor","pdf_extractor.log")


class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""
    pass


class TableExtractor:
    """
    A class for extracting tables and text from scanned PDF documents.
    
    This class provides comprehensive functionality for:
    - Converting PDF pages to images
    - Detecting table regions using computer vision
    - Extracting table data using OCR
    - Combining tables with surrounding text
    - Exporting results in multiple formats
    """
    
    SUPPORTED_FORMATS = ["csv", "json", "xlsx", "pdf"]
    DEFAULT_DPI = 300
    MIN_TABLE_WIDTH_RATIO = 0.2
    MIN_TABLE_HEIGHT_RATIO = 0.1
    TABLE_LINE_THRESHOLD = 0.3
    
    def __init__(self, dpi: int = DEFAULT_DPI):
        """
        Initialize the TableExtractor.
        
        Args:
            dpi: Resolution for PDF to image conversion
        """
        self.dpi = dpi
        self.table_counter = 1
        self._validate_dependencies()
    
    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are available."""
        try:
            import cv2
            import pytesseract
            from pdf2image import convert_from_path
        except ImportError as e:
            raise PDFExtractionError(f"Missing required dependency: {e}")
        
        # Test pytesseract
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            logger.warning("Tesseract OCR not found. Please install Tesseract.")
    
    def convert_pdf_to_images(self, pdf_path: Union[str, Path]) -> Tuple[List[np.ndarray], int]:
        """
        Convert a PDF file to a list of images.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (list of images as numpy arrays, total page count)
            
        Raises:
            PDFExtractionError: If PDF conversion fails
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            logger.info(f"Converting PDF to images: {pdf_path}")
            images = convert_from_path(str(pdf_path), dpi=self.dpi)
            image_arrays = [np.array(img) for img in images]
            
            logger.info(f"Successfully converted {len(images)} pages")
            return image_arrays, len(images)
            
        except Exception as e:
            raise PDFExtractionError(f"Failed to convert PDF to images: {e}")
    
    def _detect_lines(self, binary_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect horizontal and vertical lines in a binary image.
        
        Args:
            binary_image: Binary image array
            
        Returns:
            Tuple of (horizontal lines, vertical lines)
        """
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
        horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
        vertical_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel)
        
        return horizontal_lines, vertical_lines
    
    def _is_valid_table_region(self, contour: np.ndarray, image_shape: Tuple[int, int]) -> bool:
        """
        Determine if a contour represents a valid table region.
        
        Args:
            contour: OpenCV contour
            image_shape: Shape of the source image (height, width)
            
        Returns:
            True if the contour is a valid table region
        """
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check minimum size requirements
        min_width = image_shape[1] * self.MIN_TABLE_WIDTH_RATIO
        min_height = image_shape[0] * self.MIN_TABLE_HEIGHT_RATIO
        
        return w > min_width and h > min_height
    
    def detect_tables_and_text_regions(self, images: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Separate table and text regions from images.
        
        Args:
            images: List of input images
            
        Returns:
            Tuple of (table images, text-only images)
        """
        table_images = []
        text_images = []
        
        logger.info(f"Processing {len(images)} images for table detection")
        
        for page_num, img in enumerate(images, 1):
            try:
                # Create copies for processing
                text_image = img.copy()
                
                # Convert to grayscale
                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                else:
                    gray = img
                
                # Apply adaptive thresholding
                binary = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 15, 8
                )
                
                # Detect table structure
                horizontal_lines, vertical_lines = self._detect_lines(binary)
                table_mask = cv2.add(horizontal_lines, vertical_lines)
                table_mask = cv2.dilate(table_mask, np.ones((3, 3), np.uint8), iterations=1)
                
                # Find table contours
                contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
                
                # Process valid table regions
                table_count = 0
                for contour in contours:
                    if self._is_valid_table_region(contour, img.shape[:2]):
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Extract table region
                        table_crop = img[y:y+h, x:x+w]
                        table_images.append(table_crop)
                        table_count += 1
                        
                        # Mask table region in text image
                        cv2.rectangle(text_image, (x, y), (x+w, y+h), (255, 255, 255), -1)
                        
                        # Add table placeholder
                        label = f"Table_{page_num}_{table_count}"
                        cv2.putText(text_image, label, (x+10, y+40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
                text_images.append(text_image)
                logger.debug(f"Page {page_num}: Found {table_count} tables")
                
            except Exception as e:
                logger.error(f"Error processing page {page_num}: {e}")
                text_images.append(img)  # Use original image if processing fails
        
        logger.info(f"Detected {len(table_images)} tables across all pages")
        return table_images, text_images
    
    def _extract_table_cells(self, image: np.ndarray) -> List[List[str]]:
        """
        Extract cell data from a table image using OCR.
        
        Args:
            image: Table image array
            
        Returns:
            2D list representing table cells
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            binary = cv2.bitwise_not(binary)
            
            # Detect table structure
            kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, image.shape[1] // 80))
            vertical_lines = cv2.dilate(cv2.erode(binary, kernel_v, iterations=3), kernel_v, iterations=3)
            
            kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (image.shape[1] // 20, 1))
            horizontal_lines = cv2.dilate(cv2.erode(binary, kernel_h, iterations=3), kernel_h, iterations=3)
            
            # Create table mask
            table_mask = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            table_mask = cv2.erode(cv2.bitwise_not(table_mask), kernel, iterations=2)
            _, table_mask = cv2.threshold(table_mask, 0, 255, cv2.THRESH_OTSU)
            
            # Find cell contours
            contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
            
            # Extract text from cells
            table_data = []
            current_row = []
            last_y = -1
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if 10 < h < 100:  # Filter noise
                    # Check if we're on a new row
                    if last_y != -1 and abs(y - last_y) > 10:
                        if current_row:
                            table_data.append(current_row)
                        current_row = []
                    
                    # Extract cell text
                    cell = gray[y:y+h, x:x+w]
                    text = pytesseract.image_to_string(cell, config="--psm 6").strip()
                    current_row.append(text if text else "")
                    last_y = y
            
            if current_row:
                table_data.append(current_row)
            
            return table_data
            
        except Exception as e:
            logger.error(f"Error extracting table cells: {e}")
            return []
    
    def extract_tables(self, table_images: List[np.ndarray]) -> Dict[str, List[List[str]]]:
        """
        Extract table data from table images.
        
        Args:
            table_images: List of table images
            
        Returns:
            Dictionary mapping table keys to table data
        """
        tables = {}
        
        logger.info(f"Extracting data from {len(table_images)} tables")
        
        for i, table_image in enumerate(table_images, 1):
            try:
                table_data = self._extract_table_cells(table_image)
                if table_data:
                    tables[f"table{i}"] = table_data
                    logger.debug(f"Extracted table {i}: {len(table_data)} rows")
                else:
                    logger.warning(f"No data extracted from table {i}")
            except Exception as e:
                logger.error(f"Error extracting table {i}: {e}")
        
        return tables
    
    def extract_text(self, text_images: List[np.ndarray]) -> List[str]:
        """
        Extract text from text-only images.
        
        Args:
            text_images: List of text images
            
        Returns:
            List of extracted text strings
        """
        texts = []
        
        logger.info(f"Extracting text from {len(text_images)} images")
        
        for i, image in enumerate(text_images, 1):
            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
                text = pytesseract.image_to_string(gray, config="--oem 3 --psm 3").strip()
                texts.append(text)
                logger.debug(f"Extracted text from page {i}: {len(text)} characters")
            except Exception as e:
                logger.error(f"Error extracting text from page {i}: {e}")
                texts.append("")
        
        return texts
    
    def combine_tables_and_text(self, tables: Dict[str, List[List[str]]], texts: List[str]) -> List[str]:
        """
        Combine extracted tables with text, replacing table placeholders.
        
        Args:
            tables: Dictionary of extracted tables
            texts: List of extracted text strings
            
        Returns:
            List of combined text with embedded tables
        """
        import re
        
        combined_texts = []
        
        for text in texts:
            # Find table placeholders
            matches = re.findall(r'Table_(\d+)_(\d+)', text)
            
            for page_num, table_num in matches:
                table_key = f"table{table_num}"
                
                if table_key in tables and tables[table_key]:
                    # Format table as text
                    try:
                        table_str = tabulate(tables[table_key], headers="firstrow", tablefmt="grid")
                        text = text.replace(f"Table_{page_num}_{table_num}", f"\n{table_str}\n")
                    except Exception as e:
                        logger.error(f"Error formatting table {table_key}: {e}")
                        text = text.replace(f"Table_{page_num}_{table_num}", "[Table formatting error]")
            
            combined_texts.append(text)
        
        return combined_texts
    
    def _save_as_html_pdf(self, content: str, output_path: Path) -> bool:
        """
        Save content as PDF using HTML conversion.
        
        Args:
            content: HTML content to convert
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from xhtml2pdf import pisa
            
            with open(output_path, "wb") as output_file:
                pisa_status = pisa.CreatePDF(content.encode('utf-8'), dest=output_file)
            
            return not pisa_status.err
            
        except ImportError:
            logger.error("xhtml2pdf not installed. Cannot save as PDF.")
            return False
        except Exception as e:
            logger.error(f"Error saving PDF: {e}")
            return False
    
    def save_results(self, data: List[str], output_path: Union[str, Path], 
                    filename: str = "extracted_content", file_format: str = "csv") -> Path:
        """
        Save extracted data in the specified format.
        
        Args:
            data: Extracted text data
            output_path: Output directory path
            filename: Output filename (without extension)
            file_format: Output format (csv, json, xlsx, pdf)
            
        Returns:
            Path to the saved file
            
        Raises:
            PDFExtractionError: If saving fails
        """
        if file_format not in self.SUPPORTED_FORMATS:
            raise PDFExtractionError(f"Unsupported format: {file_format}")
        
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = output_path / f"{filename}.{file_format}"
        
        try:
            df = pd.DataFrame({"Extracted_Content": data})
            
            if file_format == "csv":
                df.to_csv(output_file, index=False, encoding='utf-8')
            elif file_format == "json":
                df.to_json(output_file, orient="records", lines=True, force_ascii=False)
            elif file_format == "xlsx":
                df.to_excel(output_file, index=False)
            elif file_format == "pdf":
                html_content = df.to_html(index=False, escape=False)
                success = self._save_as_html_pdf(html_content, output_file)
                if not success:
                    raise PDFExtractionError("Failed to save PDF")
            
            logger.info(f"Results saved to: {output_file}")
            return output_file
            
        except Exception as e:
            raise PDFExtractionError(f"Failed to save results: {e}")
    
    def process_pdf(self, pdf_path: Union[str, Path], output_path: Union[str, Path] = "./output",
                   filename: str = "extracted_content", file_format: str = "csv", 
                   issave:bool = False) -> Tuple[List[str], Optional[Path]]:
        """
        Complete PDF processing pipeline.
        
        Args:
            pdf_path: Path to input PDF file
            output_path: Output directory path
            filename: Output filename (without extension)
            file_format: Output format
            
        Returns:
            Tuple of (extracted content, saved file path)
            
        Raises:
            PDFExtractionError: If processing fails
        """
        logger.info(f"Starting PDF processing: {pdf_path}")
        
        try:
            # Convert PDF to images
            images, page_count = self.convert_pdf_to_images(pdf_path)
            logger.info(f"Converted {page_count} pages to images")
            
            # Detect tables and text regions
            table_images, text_images = self.detect_tables_and_text_regions(images)
            
            # Extract tables and text
            tables = self.extract_tables(table_images)
            texts = self.extract_text(text_images)
            
            # Combine results
            combined_content = self.combine_tables_and_text(tables, texts)
            
            if issave:
                # Save results
                saved_file = self.save_results(combined_content, output_path, filename, file_format)
                return combined_content, saved_file
            
            logger.info("PDF processing completed successfully")
            return combined_content
            
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            raise PDFExtractionError(f"Processing failed: {e}")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract tables and text from scanned PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        python pdf_extractor.py document.pdf
        python pdf_extractor.py document.pdf --output ./results --format xlsx
        python pdf_extractor.py document.pdf --dpi 200 --filename report
                """
            )
    
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("--output", "-o", default="./output", 
                       help="Output directory (default: ./output)")
    parser.add_argument("--filename", "-f", default="extracted_content",
                       help="Output filename without extension (default: extracted_content)")
    parser.add_argument("--format", "-fmt", choices=TableExtractor.SUPPORTED_FORMATS,
                       default="csv", help="Output format (default: csv)")
    parser.add_argument("--dpi", type=int, default=TableExtractor.DEFAULT_DPI,
                       help=f"DPI for PDF conversion (default: {TableExtractor.DEFAULT_DPI})")
    parser.add_argument("--tosave", "-ts", action="store_true",
                       help="Help to save a file")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Validate input file
        pdf_path = Path(args.pdf_path)
        if not pdf_path.exists():
            logger.error(f"Input file not found: {pdf_path}")
            sys.exit(1)
        
        # Initialize extractor and process PDF
        extractor = TableExtractor(dpi=args.dpi)
        result = extractor.process_pdf(
        pdf_path=pdf_path, output_path=args.output, filename=args.filename, 
        file_format=args.format, issave=args.tosave
        )

        result = extractor.process_pdf(
            pdf_path=pdf_path,
            output_path=args.output,
            filename=args.filename,
            file_format=args.format,
            issave=args.tosave
        )

        if isinstance(result, tuple):
            content, saved_file = result
        else:
            content, saved_file = result, None

        print(f"\n✅ Processing completed successfully!")
        print(f"📄 Processed: {pdf_path}")
        if saved_file:
            print(f"💾 Saved to: {saved_file}")
        else:
            print("💾 No file saved (run with --tosave to save output)")
        print(f"📊 Extracted {len(content)} content blocks")

        
    except PDFExtractionError as e:
        logger.error(f"Extraction error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()