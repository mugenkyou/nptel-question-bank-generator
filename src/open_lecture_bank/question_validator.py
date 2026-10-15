"""Psychometric validation and distractor parity audit engine.

Verifies option consistency, distractor plausibility, and duplicate detection.
(Planned component for Stage 4).
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from open_lecture_bank.config import AppConfig
from open_lecture_bank.models import MCQQuestion, QuestionBank


class ValidationReport:
    """Report detailing question bank validation results."""
    def __init__(self):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.length_bias_detected: int = 0
        self.comical_distractors_found: int = 0
        self.duplicates_found: int = 0


class QuestionValidator:
    """Audits assessment items against psychometric and structural criteria."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()

    @staticmethod
    def check_option_consistency(question: MCQQuestion) -> bool:
        """Verify that correct_answer exactly matches options[correct_option]."""
        opts = question.options.model_dump()
        c_opt = question.correct_option
        return opts.get(c_opt, "").strip() == question.correct_answer.strip()

    @staticmethod
    def calculate_length_ratio(options: Dict[str, str], correct_key: str) -> float:
        """Calculate ratio of correct option length to average distractor length."""
        c_len = len(options.get(correct_key, ""))
        other_lens = [len(v) for k, v in options.items() if k != correct_key]
        if not other_lens or sum(other_lens) == 0:
            return 1.0
        avg_other = sum(other_lens) / len(other_lens)
        return c_len / avg_other

    @staticmethod
    def compute_jaccard_similarity(text1: str, text2: str) -> float:
        """Compute word-level Jaccard similarity to detect near-duplicate questions."""
        words1 = set(re.findall(r"\b[a-zA-Z]{3,}\b", text1.lower()))
        words2 = set(re.findall(r"\b[a-zA-Z]{3,}\b", text2.lower()))
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)

    def validate_question_bank(self, bank: QuestionBank) -> ValidationReport:
        """Comprehensive verification of the complete question bank.
        
        Note: Full automated validation pipeline planned for Stage 4.
        """
        report = ValidationReport()
        return report
