"""Unit tests for StudyOrderPlanner DAG integrity."""

from open_lecture_bank.study_order import StudyOrderPlanner


def test_verify_cycle_free_valid_dag():
    """Verify that a valid topological order passes cycle check."""
    prereq_graph = {
        "T001": [],
        "T002": ["T001"],
        "T003": ["T001", "T002"],
        "T004": ["T003"]
    }
    sequence = ["T001", "T002", "T003", "T004"]
    assert StudyOrderPlanner.verify_cycle_free(prereq_graph, sequence) is True


def test_verify_cycle_free_detects_forward_dependency():
    """Verify that a sequence with forward dependency fails cycle check."""
    prereq_graph = {
        "T001": ["T003"],  # T001 depends on T003 which appears later!
        "T002": ["T001"],
        "T003": []
    }
    sequence = ["T001", "T002", "T003"]
    assert StudyOrderPlanner.verify_cycle_free(prereq_graph, sequence) is False
