"""
Audio Input Handler — ASR pipeline using Whisper.
"""

import os
import re
import tempfile
from typing import Dict, Any

ASR_CONFIDENCE_THRESHOLD = 0.6

# Math phrase normalization rules
MATH_PHRASE_MAP = {
    r"square root of (\w+)": r"sqrt(\1)",
    r"(\w+) squared": r"\1^2",
    r"(\w+) cubed": r"\1^3",
    r"(\w+) raised to the power (\w+)": r"\1^\2",
    r"(\w+) raised to (\w+)": r"\1^\2",
    r"integral of": "integrate",
    r"derivative of": "d/dx",
    r"d y by d x": "dy/dx",
    r"dy by dx": "dy/dx",
    r"d by d x": "d/dx",
    r"d by dx": "d/dx",
    r"greater than or equal to": ">=",
    r"less than or equal to": "<=",
    r"greater than": ">",
    r"less than": "<",
    r"not equal to": "!=",
    r"plus or minus": "+-",
    r"minus or plus": "-+",
}


class AudioHandler:
    """Handles audio input with ASR transcription."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("WHISPER_MODEL", "base")
        self.name = "Audio Handler"
        self._model = None

    def _load_model(self):
        """Lazy-load the Whisper model."""
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self.model_name)

    def process_bytes(self, audio_bytes: bytes, filename: str = "recorded.wav") -> Dict[str, Any]:
        """
        Process raw audio bytes (e.g. from a live recording widget).

        Args:
            audio_bytes: Raw audio data as bytes.
            filename: Name hint for the temp file extension.

        Returns:
            Dict with transcript, confidence, and metadata.
        """
        suffix = "." + filename.rsplit(".", 1)[-1] if "." in filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            audio_path = tmp.name
        return self.process(audio_path)

    def process(self, audio_file) -> Dict[str, Any]:
        """
        Process an uploaded audio file and transcribe it.

        Args:
            audio_file: Uploaded file object or file path string.

        Returns:
            Dict with transcript, confidence, and metadata.
        """
        # Save uploaded file to temp if needed
        if isinstance(audio_file, str):
            audio_path = audio_file
        else:
            suffix = ".wav"
            name = getattr(audio_file, "name", "audio.wav")
            if name.endswith(".mp3"):
                suffix = ".mp3"
            elif name.endswith(".m4a"):
                suffix = ".m4a"

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio_file.getvalue())
                audio_path = tmp.name

        try:
            result = self._transcribe(audio_path)
        except Exception as e:
            result = {
                "text": "",
                "confidence": 0.0,
                "error": f"Transcription failed: {str(e)}",
            }

        # Normalize math phrases
        if result.get("text"):
            result["raw_transcript"] = result["text"]
            result["text"] = self._normalize_math(result["text"])

        result["input_type"] = "audio"
        result["audio_path"] = audio_path
        result["needs_review"] = result.get("confidence", 0) < ASR_CONFIDENCE_THRESHOLD
        result["raw_input"] = audio_path

        return result

    def _transcribe(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio using Whisper."""
        self._load_model()

        result = self._model.transcribe(audio_path)

        text = result.get("text", "").strip()

        # Estimate confidence from segments
        segments = result.get("segments", [])
        if segments:
            avg_logprob = sum(s.get("avg_logprob", -1) for s in segments) / len(segments)
            # Convert log probability to a 0-1 confidence score
            # avg_logprob is typically between -1 (low) and 0 (high)
            confidence = max(0, min(1, 1 + avg_logprob))
        else:
            confidence = 0.5 if text else 0.0

        return {
            "text": text,
            "confidence": confidence,
            "engine": "whisper",
            "model": self.model_name,
        }

    def _normalize_math(self, text: str) -> str:
        """Normalize spoken math phrases to symbolic notation."""
        result = text
        for pattern, replacement in MATH_PHRASE_MAP.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
