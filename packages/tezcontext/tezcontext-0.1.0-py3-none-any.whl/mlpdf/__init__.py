"""
mlpdf: Access the bundled 'All ML programs' PDF.
"""

import os

__all__ = ["get_pdf_path"]

def get_pdf_path():
    """Returns the absolute path to the bundled PDF file."""
    return os.path.join(os.path.dirname(__file__), "data", "All_ML_programs.pdf") 