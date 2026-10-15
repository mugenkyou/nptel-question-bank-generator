"""PDF extraction engine for Open Lecture Bank.

Extracts page-indexed text, computes file hashes, and flags visual-only slides.
(Planned component for Stage 2).
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from open_lecture_bank.config import AppConfig


class ExtractedPage:
    """Represents text extracted from a single PDF page."""
    def __init__(self, page_number: int, text: str, char_count: int, is_low_text: bool):
        self.page_number = page_number
        self.text = text
        self.char_count = char_count
        self.is_low_text = is_low_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page": self.page_number,
            "char_count": self.char_count,
            "is_low_text": self.is_low_text,
            "text": self.text,
        }


class PDFExtractor:
    """Engine responsible for extracting structured text from course slide decks."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()

    @staticmethod
    def compute_sha256(file_path: Path) -> str:
        """Calculate SHA-256 hash to detect duplicate lecture slides."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def extract_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Extract page-by-page text from a single PDF.
        
        Note: Implementation using PyMuPDF (fitz) is planned for Stage 2.
        """
        raise NotImplementedError("PDFExtractor.extract_pdf is planned for Stage 2 implementation.")

    def scan_directory(self, input_dir: Path) -> List[Path]:
        """Discover and inventory all PDF files in the target directory."""
        if not input_dir.exists():
            return []
        return sorted([p for p in input_dir.rglob("*.pdf") if p.is_file()])
