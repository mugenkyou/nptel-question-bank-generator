# Agent Guidelines for Open Lecture Bank

This document establishes operational conventions and engineering rules for automated coding agents working in the `open-lecture-bank` repository.

---

## 1. System Overview & Architecture

Open Lecture Bank transforms collections of academic lecture slide PDFs into structured, psychometrically validated MCQ question banks and prerequisite learning roadmaps.

The pipeline comprises six modular stages:
1. **PDF Extractor** (`pdf_extractor.py`): Ingestion, page text extraction, slide classification, SHA-256 deduplication.
2. **Topic Analyzer** (`topic_analyzer.py`): Concept mining, definition extraction, prerequisite relationship deduction.
3. **Question Generator** (`question_generator.py`): 4-option single-answer MCQ synthesis with balanced distractors and rationales.
4. **Question Validator** (`question_validator.py`): Psychometric auditing (distractor length parity, duplicate detection via Jaccard similarity, option consistency).
5. **Study Order Planner** (`study_order.py`): Topological sorting into a 10-stage Directed Acyclic Graph (DAG).
6. **Exporter** (`exporter.py`): JSON serialization of `question_bank.json` and `processing_manifest.json`.

Pipeline execution is coordinated via `pipeline.py` with CLI entry points defined in `cli.py`.

---

## 2. Implementation Status Baseline

Before modifying any file, verify the actual implementation status against `docs/ROADMAP.md`:

| Component | Status | Details |
| :--- | :--- | :--- |
| `models.py` | **Implemented** | Core Pydantic v2 data models with field validations. |
| `config.py` | **Implemented** | Settings loader supporting JSON and `.env`. |
| `exporter.py` | **Implemented** | JSON serializers for QuestionBank and ProcessingManifest. |
| `question_validator.py` | **Partial** | Static audit helpers implemented; full bank audit is stubbed. |
| `study_order.py` | **Partial** | DAG cycle check implemented; topological sequencer is stubbed. |
| `pdf_extractor.py` | **Scaffolded** | SHA-256 and directory scanner implemented; PyMuPDF extractor is stubbed. |
| `topic_analyzer.py` | **Planned** | Method stubs raising `NotImplementedError`. |
| `question_generator.py` | **Planned** | Method stubs raising `NotImplementedError`. |
| `pipeline.py` | **Planned** | Method stubs raising `NotImplementedError`. |
| `cli.py` | **Scaffolded** | Click CLI commands defined with informational stubs. |

**Rule**: Do not assume a module is functional simply because its file or test exists. Inspect implementation code directly.

---

## 3. Engineering & Code Standards

- **Python & Packaging**: Python 3.10+ required. Packaging configured in `pyproject.toml` (PEP 517/518).
- **Type Safety**: Strictly typed with type hints (`typing` and Pydantic v2). All data entities must inherit from or validate through `open_lecture_bank.models`.
- **Formatting**: Adhere to Black formatting standards (line length 100).
- **Encoding**: All file I/O must explicitly use `encoding="utf-8"`.
- **Provider Agnosticism**: AI interactions must be abstracted behind provider interfaces (`none`, `openai`, `gemini`, `anthropic`, `local_ollama`). Never hardcode a specific model or vendor into core pipeline stages.
- **Universal Subjects**: The engine must remain subject-agnostic. Never introduce domain-specific heuristics that break support for arbitrary disciplines.

---

## 4. Assessment Integrity & Pedagogical Contracts

All generated questions must satisfy the following constraints:
1. **Four Options Only**: Exactly options `A`, `B`, `C`, and `D`.
2. **Single Correct Answer**: `correct_option` must be one of `A`, `B`, `C`, `D`, and `correct_answer` must equal `options[correct_option]`.
3. **Evidence Grounding**: Every question must cite valid source pages within PDF limits and provide verbatim or faithful textual evidence.
4. **Distractor Parity**: Distractor character lengths must stay within a 1.5 ratio of the correct answer to prevent length-cueing.
5. **No Absurd Distractors**: Distractors must be plausible academic misconceptions, not jokes or impossible assertions.
6. **Key Distribution**: Correct answer keys should be distributed naturally across options without predictable patterns.

---

## 5. Checkpointing & State Persistence

- Courses may contain 50–100+ lectures. Pipeline execution must be resilient to interruption.
- Page extractions must save to `data/intermediate/extracted/<sha256>_extracted.json`.
- Batched question generation must save to `data/intermediate/batches/batch_XX.json`.
- Operations must support resuming from existing checkpoints without re-processing completed inputs.

---

## 6. Safety & Non-Destructive Principles

- **Preserve User Assets**: Never delete, move, or modify source PDFs in `data/input/` or outputs in `data/output/` unless explicitly instructed.
- **No Fabricated Evidence or Status**:
  - Never fake test runs, execution logs, or source citations.
  - If a test cannot be executed because dependencies or runners are absent, report that fact explicitly.
- **Credential Safety**: Never commit API keys, secrets, or `.env` files. Ensure `.gitignore` is preserved.
- **Incremental Changes**: Make minimal, coherent modifications with clear acceptance criteria and corresponding test coverage.
