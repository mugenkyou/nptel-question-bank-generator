"""Configuration management for Open Lecture Bank."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class DirectoryConfig(BaseModel):
    """Configured directory paths."""
    input: str = "./data/input"
    output: str = "./data/output"
    intermediate: str = "./data/intermediate"
    logs: str = "./logs"


class ExtractionConfig(BaseModel):
    """PDF extraction parameters."""
    char_threshold_per_page: int = 50
    ocr_enabled: bool = False
    max_pages_per_pdf: int = 200
    ignore_blank_slides: bool = True


class GenerationConfig(BaseModel):
    """MCQ generation settings."""
    questions_per_topic: int = 3
    options_per_question: int = 4
    target_difficulty_distribution: Dict[str, float] = Field(
        default_factory=lambda: {"easy": 0.25, "medium": 0.50, "hard": 0.25}
    )
    enable_distractor_parity_check: bool = True
    max_distractor_length_ratio: float = 1.5


class ValidationConfig(BaseModel):
    """Question validation criteria."""
    enforce_single_correct_answer: bool = True
    disallow_absurd_distractors: bool = True
    min_explanation_words: int = 15
    check_page_bounds: bool = True
    similarity_threshold_duplicate_flag: float = 0.65


class StudyOrderConfig(BaseModel):
    """Curriculum sequencing configuration."""
    enforce_strict_dag: bool = True
    max_stages: int = 10


class AppConfig(BaseModel):
    """Master application configuration."""
    project_name: str = "Open Lecture Bank"
    version: str = "0.1.0"
    ai_provider: str = Field(default="none")
    ai_api_key: Optional[str] = None
    ai_model_name: Optional[str] = None
    batch_size: int = 3
    directories: DirectoryConfig = Field(default_factory=DirectoryConfig)
    extraction: ExtractionConfig = Field(default_factory=ExtractionConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    study_order: StudyOrderConfig = Field(default_factory=StudyOrderConfig)

    @classmethod
    def load_from_json(cls, config_path: Path) -> "AppConfig":
        """Load configuration from a JSON settings file."""
        if not config_path.exists():
            return cls()
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
