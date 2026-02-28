"""
Image Input Handler — OCR pipeline using Tesseract with EasyOCR fallback.
"""

import os
import tempfile
from typing import Dict, Any, Optional

from PIL import Image

OCR_CONFIDENCE_THRESHOLD = 70.0


class ImageHandler:
    """Handles image input with OCR extraction."""

    def __init__(self, engine: str = None):
        self.engine = engine or os.getenv("OCR_ENGINE", "tesseract")
        self.name = "Image Handler"

    def process(self, image_file) -> Dict[str, Any]:
        """
        Process an uploaded image and extract text using OCR.

        Args:
            image_file: Uploaded file object (from Streamlit) or file path string.

        Returns:
            Dict with extracted text, confidence, and metadata.
        """
        # Save uploaded file to temp if needed
        if isinstance(image_file, str):
            image_path = image_file
        else:
            suffix = ".png"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(image_file.getvalue())
                image_path = tmp.name

        # Try primary OCR engine
        try:
            if self.engine == "tesseract":
                result = self._ocr_tesseract(image_path)
            else:
                result = self._ocr_easyocr(image_path)
        except Exception as e:
            # Fallback to other engine
            try:
                if self.engine == "tesseract":
                    result = self._ocr_easyocr(image_path)
                else:
                    result = self._ocr_tesseract(image_path)
            except Exception as e2:
                result = {
                    "text": "",
                    "confidence": 0.0,
                    "error": f"Both OCR engines failed: {str(e)}, {str(e2)}",
                }

        result["input_type"] = "image"
        result["image_path"] = image_path
        result["needs_review"] = result.get("confidence", 0) < OCR_CONFIDENCE_THRESHOLD
        result["raw_input"] = image_path

        return result

    def _ocr_tesseract(self, image_path: str) -> Dict[str, Any]:
        """Run OCR using Tesseract."""
        import pytesseract

        image = Image.open(image_path)

        # Get detailed data for confidence
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        # Extract text
        text = pytesseract.image_to_string(image).strip()

        # Compute average confidence (filter out -1 entries)
        confidences = [int(c) for c in data["conf"] if int(c) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return {
            "text": text,
            "confidence": avg_confidence,
            "engine": "tesseract",
        }

    def _ocr_easyocr(self, image_path: str) -> Dict[str, Any]:
        """Run OCR using EasyOCR."""
        import easyocr

        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(image_path)

        # Combine text and compute average confidence
        texts = []
        confidences = []
        for (bbox, text, conf) in results:
            texts.append(text)
            confidences.append(conf)

        combined_text = " ".join(texts)
        avg_confidence = (sum(confidences) / len(confidences) * 100) if confidences else 0.0

        return {
            "text": combined_text,
            "confidence": avg_confidence,
            "engine": "easyocr",
        }
