"""Unit tests for core Pydantic data models."""

import pytest
from pydantic import ValidationError
from open_lecture_bank.models import (
    DifficultyEnum,
    QuestionTypeEnum,
    ImportanceEnum,
    ProcessingStatusEnum,
    SourceReference,
    MCQOptionSet,
    MCQOptionExplanations,
    MCQQuestion,
    Topic,
    Lecture,
    PrerequisiteTopicEntry,
    QuestionBank,
)


def test_valid_source_reference():
    """Verify valid source reference instantiation."""
    src = SourceReference(filename="lecture_01.pdf", pages=[1, 2], evidence="Course scope and objectives.")
    assert src.filename == "lecture_01.pdf"
    assert src.pages == [1, 2]
    assert src.evidence == "Course scope and objectives."


def test_empty_pages_raises_validation_error():
    """Verify that empty pages list raises a validation error."""
    with pytest.raises(ValidationError):
        SourceReference(filename="lecture_01.pdf", pages=[], evidence="Invalid empty pages.")


def test_valid_mcq_question():
    """Verify valid MCQ question instantiation."""
    q = MCQQuestion(
        question_id="L001-T001-Q001",
        question_type=QuestionTypeEnum.CONCEPTUAL,
        difficulty=DifficultyEnum.MEDIUM,
        question="What is the primary objective of watershed management?",
        options=MCQOptionSet(
            A="Maximizing flood peaks",
            B="Soil and water conservation for sustainable production",
            C="Eliminating all vegetation",
            D="Paving drainage channels with asphalt"
        ),
        correct_option="B",
        correct_answer="Soil and water conservation for sustainable production",
        explanation="Watershed management integrates land and water conservation to enhance production and ecological balance.",
        option_explanations=MCQOptionExplanations(
            A="Incorrect: Watershed management aims to attenuate flood peaks.",
            B="Correct: Sustainable soil and water management is the primary goal.",
            C="Incorrect: Vegetation is vital for soil retention.",
            D="Incorrect: Paving accelerates destructive runoff."
        ),
        source=SourceReference(filename="lecture_01.pdf", pages=[3, 4], evidence="Watershed goals include soil and water conservation.")
    )
    assert q.question_id == "L001-T001-Q001"
    assert q.correct_option == "B"
    assert q.options.B == q.correct_answer


def test_prerequisite_topic_entry():
    """Verify prerequisite topic entry initialization."""
    entry = PrerequisiteTopicEntry(
        sequence_number=1,
        topic_id="L001-T001",
        lecture_id="L001",
        source_file="lecture_01.pdf",
        canonical_topic_name="Hydrological Principles",
        recommended_stage="Stage 1: Fundamentals",
        prerequisite_topic_ids=[],
        learning_objectives=["Understand basic water balance."],
        associated_question_ids=["L001-T001-Q001"],
        pedagogical_rationale="Foundational concept."
    )
    assert entry.sequence_number == 1
    assert entry.topic_id == "L001-T001"
    assert entry.prerequisite_topic_ids == []
