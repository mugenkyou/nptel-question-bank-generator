"""Export engine for question banks and processing manifests.

Serializes validated assessment banks to standard JSON format.
(Planned component for Stage 5).
"""

import json
from pathlib import Path
from typing import Optional
from open_lecture_bank.config import AppConfig
from open_lecture_bank.models import QuestionBank, ProcessingManifest


class Exporter:
    """Handles serialization of question banks and operational manifests."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()

    def export_question_bank(self, bank: QuestionBank, output_file: Path) -> None:
        """Serialize QuestionBank model to formatted JSON file."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(bank.model_dump(), f, indent=2, ensure_ascii=False)

    def export_manifest(self, manifest: ProcessingManifest, output_file: Path) -> None:
        """Serialize ProcessingManifest model to formatted JSON file."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(), f, indent=2, ensure_ascii=False)
