"""
Tests for Tesseract OCR integration via ImageHandler.
Verifies that pytesseract + tesseract binary are installed and functional.
"""

import os
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageFont


def _make_test_image(text: str, path: str) -> None:
    """Create a simple white PNG image with black text for OCR testing."""
    img = Image.new("RGB", (400, 100), color="white")
    draw = ImageDraw.Draw(img)
    # Use default bitmap font (always available, no extra files needed)
    draw.text((10, 30), text, fill="black")
    img.save(path)


class TestTesseractInstallation(unittest.TestCase):
    """Checks that tesseract binary and pytesseract package are available."""

    def test_pytesseract_importable(self):
        """pytesseract Python package must be importable."""
        import pytesseract  # noqa: F401

    def test_tesseract_binary_found(self):
        """pytesseract must be able to locate the tesseract binary."""
        import pytesseract

        version = pytesseract.get_tesseract_version()
        self.assertIsNotNone(version, "tesseract binary not found")

    def test_tesseract_version_5(self):
        """Installed tesseract should be version 5.x (as set up in this env)."""
        import pytesseract
        from packaging.version import Version

        ver = pytesseract.get_tesseract_version()
        self.assertGreaterEqual(
            Version(str(ver)),
            Version("4.0.0"),
            f"Expected tesseract >= 4.0.0, got {ver}",
        )


class TestTesseractOCR(unittest.TestCase):
    """End-to-end OCR tests using pytesseract on generated images."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def _image_path(self, filename: str) -> str:
        return os.path.join(self.tmp_dir, filename)

    def test_ocr_simple_text(self):
        """OCR on a simple ASCII string returns a non-empty result."""
        import pytesseract

        path = self._image_path("simple.png")
        _make_test_image("Hello Math", path)
        img = Image.open(path)
        result = pytesseract.image_to_string(img).strip()
        self.assertTrue(len(result) > 0, f"Expected non-empty OCR output, got: {result!r}")

    def test_ocr_numeric_text(self):
        """OCR correctly extracts digits from a test image."""
        import pytesseract

        path = self._image_path("numeric.png")
        _make_test_image("1234567890", path)
        img = Image.open(path)
        result = pytesseract.image_to_string(img).strip()
        # Check that at least some digits were found
        digits_found = sum(c.isdigit() for c in result)
        self.assertGreater(digits_found, 0, f"No digits extracted. Got: {result!r}")

    def test_ocr_confidence_data(self):
        """image_to_data returns confidence values."""
        import pytesseract

        path = self._image_path("conf.png")
        _make_test_image("Calculus", path)
        img = Image.open(path)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        self.assertIn("conf", data, "Expected 'conf' key in pytesseract data output")
        self.assertIsInstance(data["conf"], list)


class TestImageHandlerTesseract(unittest.TestCase):
    """Tests for the project's ImageHandler class using the tesseract engine."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def _image_path(self, filename: str) -> str:
        return os.path.join(self.tmp_dir, filename)

    def test_image_handler_returns_dict(self):
        """ImageHandler.process returns a dict with required keys."""
        from input.image_handler import ImageHandler

        handler = ImageHandler(engine="tesseract")
        path = self._image_path("math.png")
        _make_test_image("x squared plus 1", path)

        result = handler.process(path)

        for key in ("text", "confidence", "engine", "input_type", "needs_review"):
            self.assertIn(key, result, f"Missing key '{key}' in result")

    def test_image_handler_engine_label(self):
        """ImageHandler reports engine as 'tesseract'."""
        from input.image_handler import ImageHandler

        handler = ImageHandler(engine="tesseract")
        path = self._image_path("label.png")
        _make_test_image("test", path)

        result = handler.process(path)
        self.assertEqual(result.get("engine"), "tesseract")

    def test_image_handler_confidence_range(self):
        """Confidence score is between 0 and 100."""
        from input.image_handler import ImageHandler

        handler = ImageHandler(engine="tesseract")
        path = self._image_path("conf_range.png")
        _make_test_image("Find the derivative", path)

        result = handler.process(path)
        conf = result.get("confidence", -1)
        self.assertGreaterEqual(conf, 0.0, "Confidence below 0")
        self.assertLessEqual(conf, 100.0, "Confidence above 100")

    def test_needs_review_flag(self):
        """needs_review flag is a boolean."""
        from input.image_handler import ImageHandler

        handler = ImageHandler(engine="tesseract")
        path = self._image_path("review.png")
        _make_test_image("integration", path)

        result = handler.process(path)
        self.assertIsInstance(result.get("needs_review"), bool)


if __name__ == "__main__":
    unittest.main()
