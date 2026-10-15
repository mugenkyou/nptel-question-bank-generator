"""Unit tests for QuestionValidator psychometric checks."""

from open_lecture_bank.models import (
    DifficultyEnum,
    QuestionTypeEnum,
    SourceReference,
    MCQOptionSet,
    MCQOptionExplanations,
    MCQQuestion,
)
from open_lecture_bank.question_validator import QuestionValidator


def test_option_consistency_check_passes():
    """Verify that correct option text matching correct answer returns True."""
    q = MCQQuestion(
        question_id="L001-T001-Q001",
        question_type=QuestionTypeEnum.DEFINITION,
        difficulty=DifficultyEnum.EASY,
        question="What is porosity?",
        options=MCQOptionSet(A="Void ratio", B="Ratio of void volume to total volume", C="Permeability", D="Transmissivity"),
        correct_option="B",
        correct_answer="Ratio of void volume to total volume",
        explanation="Porosity measures void space.",
        option_explanations=MCQOptionExplanations(A="No", B="Yes", C="No", D="No"),
        source=SourceReference(filename="lecture_01.pdf", pages=[1], evidence="Porosity definition.")
    )
    assert QuestionValidator.check_option_consistency(q) is True


def test_calculate_length_ratio():
    """Verify option length ratio calculation."""
    # Balanced options
    opts_balanced = {"A": "First option text", "B": "Second option text", "C": "Third option text", "D": "Fourth option text"}
    ratio = QuestionValidator.calculate_length_ratio(opts_balanced, "A")
    assert 0.9 <= ratio <= 1.1

    # Length-biased option
    opts_biased = {
        "A": "Short option",
        "B": "This is an extremely long and detailed correct answer with multiple descriptive clauses explaining everything",
        "C": "Short option",
        "D": "Short option"
    }
    ratio_biased = QuestionValidator.calculate_length_ratio(opts_biased, "B")
    assert ratio_biased > 3.0


def test_jaccard_similarity():
    """Verify Jaccard similarity computation for duplicate detection."""
    text1 = "Which branch of hydrology deals with groundwater movement?"
    text2 = "Which branch of hydrology deals with groundwater movement?"
    text3 = "What is the primary function of a solar panel in space?"

    assert QuestionValidator.compute_jaccard_similarity(text1, text2) == 1.0
    assert QuestionValidator.compute_jaccard_similarity(text1, text3) < 0.2
