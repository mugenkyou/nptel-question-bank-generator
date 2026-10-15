"""Pipeline coordinator with persistent intermediate checkpointing.

Coordinates extraction, analysis, generation, validation, and export.
(Planned component for Stage 5).
"""

from pathlib import Path
from typing import Optional
from open_lecture_bank.config import AppConfig


class LecturePipeline:
    """Orchestrates end-to-end processing across modular pipeline stages."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()

    def run(self, input_dir: Path, output_dir: Path) -> None:
        """Run the end-to-end processing pipeline.
        
        Note: Full pipeline orchestration planned for Stage 5.
        """
        raise NotImplementedError("LecturePipeline.run is planned for Stage 5 implementation.")

    def resume_from_checkpoint(self, intermediate_dir: Path) -> None:
        """Resume incomplete processing from last confirmed completed batch."""
        raise NotImplementedError("LecturePipeline.resume_from_checkpoint planned for Stage 5.")
