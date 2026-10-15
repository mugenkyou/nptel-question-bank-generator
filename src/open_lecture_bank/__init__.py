"""Open Lecture Bank: Universal engine to generate MCQ banks and learning roadmaps from lecture PDFs."""

__version__ = "0.1.0"
__author__ = "Open Lecture Bank Contributors"
__license__ = "MIT"

from open_lecture_bank.models import (
    MCQOptionSet,
    MCQOptionExplanations,
    MCQQuestion,
    Topic,
    Lecture,
    PrerequisiteTopicEntry,
    QuestionBank,
    ProcessingManifest,
)
from open_lecture_bank.config import AppConfig

__all__ = [
    "AppConfig",
    "MCQOptionSet",
    "MCQOptionExplanations",
    "MCQQuestion",
    "Topic",
    "Lecture",
    "PrerequisiteTopicEntry",
    "QuestionBank",
    "ProcessingManifest",
]
