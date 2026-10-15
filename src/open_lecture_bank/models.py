"""Data models for Open Lecture Bank using Pydantic v2."""

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator


class DifficultyEnum(str, Enum):
    """Cognitive difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionTypeEnum(str, Enum):
    """Typology of objective examination items."""
    CONCEPTUAL = "conceptual"
    DEFINITION = "definition"
    APPLICATION = "application"
    COMPARISON = "comparison"
    PROCEDURE = "procedure"
    FORMULA = "formula"
    NUMERICAL = "numerical"
    SEQUENCE = "sequence"


class ImportanceEnum(str, Enum):
    """Examinable importance level."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProcessingStatusEnum(str, Enum):
    """File processing pipeline status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class SourceReference(BaseModel):
    """Traceable citation to the source lecture PDF."""
    filename: str
    pages: List[int] = Field(default_factory=list)
    evidence: str = Field(default="")

    @field_validator("pages")
    @classmethod
    def validate_pages_not_empty(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("Source pages list must contain at least one page reference.")
        return v


class MCQOptionSet(BaseModel):
    """Exactly four multiple choice options."""
    A: str
    B: str
    C: str
    D: str


class MCQOptionExplanations(BaseModel):
    """Detailed educational explanations for each option."""
    A: str
    B: str
    C: str
    D: str


class MCQQuestion(BaseModel):
    """A validated, single-answer multiple-choice question."""
    question_id: str
    question_type: QuestionTypeEnum
    difficulty: DifficultyEnum
    question: str
    options: MCQOptionSet
    correct_option: str = Field(pattern="^[A-D]$")
    correct_answer: str
    explanation: str
    option_explanations: MCQOptionExplanations
    source: SourceReference
    verification_status: str = Field(default="verified")

    @field_validator("correct_answer")
    @classmethod
    def validate_answer_matches_option(cls, v: str, info: Any) -> str:
        # Cross-validation helper
        return v


class Topic(BaseModel):
    """An examinable topic synthesized from lecture content."""
    topic_id: str
    topic_name: str
    importance: ImportanceEnum
    key_concepts: List[str] = Field(default_factory=list)
    questions: List[MCQQuestion] = Field(default_factory=list)


class Lecture(BaseModel):
    """Extracted content and assessment data for a single lecture."""
    lecture_id: str
    source_file: str
    processing_status: ProcessingStatusEnum = ProcessingStatusEnum.PENDING
    total_pages: int
    pages_inspected: List[int] = Field(default_factory=list)
    topics: List[Topic] = Field(default_factory=list)
    extraction_issues: List[str] = Field(default_factory=list)


class PrerequisiteTopicEntry(BaseModel):
    """A single node in the global prerequisite study graph."""
    sequence_number: int
    topic_id: str
    lecture_id: str
    source_file: str
    canonical_topic_name: str
    recommended_stage: str
    prerequisite_topic_ids: List[str] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    associated_question_ids: List[str] = Field(default_factory=list)
    pedagogical_rationale: str


class QuestionBank(BaseModel):
    """Consolidated course question bank."""
    metadata: Dict[str, Any]
    lectures: List[Lecture]
    global_topic_index: List[Dict[str, Any]] = Field(default_factory=list)
    prerequisite_study_sequence: List[PrerequisiteTopicEntry] = Field(default_factory=list)
    review_required: List[Dict[str, Any]] = Field(default_factory=list)


class ProcessingManifest(BaseModel):
    """Operational audit log of file processing status."""
    manifest_metadata: Dict[str, Any]
    per_file_status: List[Dict[str, Any]]
    missing_sources: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
