# vHTML - Visual HTML Generator

A modular system for converting PDF documents to HTML with OCR and layout analysis.

## Features

- PDF to image conversion with preprocessing (denoise, deskew)
- Document layout analysis and segmentation
- OCR with multi-language support (Polish, English, German)
- Language detection and confidence scoring
- HTML generation with embedded images and metadata
- Batch processing capabilities
- Command-line interface

## Installation

### Prerequisites

- Python 3.8+
- Tesseract OCR
- Poppler utilities

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/fin-officer/vhtml.git
cd vhtml

# Install with Poetry
make install
```

### Manual Installation

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-pol tesseract-ocr-eng tesseract-ocr-deu poppler-utils

# Install Python dependencies
pip install poetry
poetry install
```

## Validate Installation

To verify that all dependencies are correctly installed:

```bash
make validate
```

or

```bash
python scripts/validate_installation.py
```

## Usage

### Command Line Interface

```bash
# Process a single PDF file
poetry run python -m vhtml.main /path/to/document.pdf -o output_directory

# Process a directory of PDF files
poetry run python -m vhtml.main /path/to/pdf_directory -b -o output_directory

# Process and open in browser
poetry run python -m vhtml.main /path/to/document.pdf -v
```

### Integration Test

```bash
# Run the integration test with your PDF file
poetry run python scripts/test_integration.py /path/to/document.pdf -v
```

### Python API

```python
from vhtml.main import DocumentAnalyzer

# Initialize the analyzer
analyzer = DocumentAnalyzer()

# Process a document
html_path = analyzer.analyze_document("document.pdf", "output_dir")

# Print the path to the generated HTML
print(f"Generated HTML: {html_path}")
```

## Core Components

- **PDFProcessor**: Handles PDF to image conversion and preprocessing
- **LayoutAnalyzer**: Analyzes document layout and segments content blocks
- **OCREngine**: Performs OCR with language detection and confidence scoring
- **HTMLGenerator**: Generates HTML with embedded images and styling
- **DocumentAnalyzer**: Integrates all components into a complete workflow

## Project Structure

```
vhtml/
├── vhtml/
│   ├── core/
│   │   ├── pdf_processor.py
│   │   ├── layout_analyzer.py
│   │   ├── ocr_engine.py
│   │   └── html_generator.py
│   └── main.py
├── scripts/
│   ├── validate_installation.py
│   └── test_integration.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION.md
│   └── PROJECT_STRUCTURE.md
├── Makefile
├── pyproject.toml
└── README.md
```

## Development

```bash
# Setup development environment
make setup

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Build package
make build
```

## Documentation

For more detailed information, see the documentation files:

- [Architecture](docs/ARCHITECTURE.md)
- [Implementation](docs/IMPLEMENTATION.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
