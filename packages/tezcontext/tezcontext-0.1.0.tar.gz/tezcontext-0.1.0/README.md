# mlpdf

A simple Python library to access the bundled 'All ML programs' PDF.

## Installation

```bash
pip install .
```

## Usage

```python
import mlpdf
pdf_path = mlpdf.get_pdf_path()
print("PDF is at:", pdf_path)
```

This will print the path to the PDF file included in the package. 