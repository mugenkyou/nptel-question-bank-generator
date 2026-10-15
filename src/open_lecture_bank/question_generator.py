"""Structured multiple-choice question generation engine.

Produces four-option MCQs adhering to assessment standards.
(Planned component for Stage 3).
"""

from typing import List, Dict, Any, Optional
from open_lecture_bank.config import AppConfig
from open_lecture_bank.models import Topic, MCQQuestion


class QuestionGenerator:
    """Generates objective, single-answer MCQs with 4 options and complete explanations."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()

    def generate_for_topic(self, topic: Topic, lecture_context: Dict[str, Any]) -> List[MCQQuestion]:
        """Generate high-quality examinable MCQs covering a specific topic.
        
        Note: Implementation planned for Stage 3.
        """
        raise NotImplementedError("QuestionGenerator.generate_for_topic is planned for Stage 3 implementation.")

    def balance_option_lengths(self, options: Dict[str, str], correct_key: str) -> Dict[str, str]:
        """Symmetrize option lengths to prevent length-based answer cueing."""
        raise NotImplementedError("QuestionGenerator.balance_option_lengths is planned for Stage 3 implementation.")
