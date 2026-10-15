"""Unit tests for Exporter serialization."""

import json
from pathlib import Path
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
    QuestionBank,
    ProcessingManifest,
)
from open_lecture_bank.exporter import Exporter


def test_export_question_bank(tmp_path: Path):
    """Verify exporting a QuestionBank to JSON."""
    q = MCQQuestion(
        question_id="L001-T001-Q001",
        question_type=QuestionTypeEnum.CONCEPTUAL,
        difficulty=DifficultyEnum.MEDIUM,
        question="What is the hydrological cycle?",
        options=MCQOptionSet(A="Continuous water circulation", B="Static water storage", C="Atmospheric heating", D="Groundwater salinity"),
        correct_option="A",
        correct_answer="Continuous water circulation",
        explanation="The hydrological cycle is continuous.",
        option_explanations=MCQOptionExplanations(A="Yes", B="No", C="No", D="No"),
        source=SourceReference(filename="lecture_01.pdf", pages=[1], evidence="Water cycle.")
    )
    topic = Topic(topic_id="L001-T001", topic_name="Water Cycle", importance=ImportanceEnum.HIGH, questions=[q])
    lecture = Lecture(lecture_id="L001", source_file="lecture_01.pdf", processing_status=ProcessingStatusEnum.COMPLETE, total_pages=5, topics=[topic])
    bank = QuestionBank(metadata={"title": "Test Course", "total_questions": 1}, lectures=[lecture])

    exporter = Exporter()
    output_file = tmp_path / "test_qb.json"
    exporter.export_question_bank(bank, output_file)

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["metadata"]["title"] == "Test Course"
    assert len(data["lectures"]) == 1


def test_export_manifest(tmp_path: Path):
    """Verify exporting a ProcessingManifest to JSON."""
    manifest = ProcessingManifest(
        manifest_metadata={"course": "Test Course", "pdf_count": 1},
        per_file_status=[{"file": "lecture_01.pdf", "status": "complete", "pages": 5}],
        missing_sources=[],
        limitations=[]
    )

    exporter = Exporter()
    output_file = tmp_path / "test_manifest.json"
    exporter.export_manifest(manifest, output_file)

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["manifest_metadata"]["pdf_count"] == 1
