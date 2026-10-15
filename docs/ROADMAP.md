# Open Lecture Bank: Development Roadmap

This roadmap outlines the phased development of Open Lecture Bank from its foundational scaffold into a production-grade, open-source educational platform.

---

## Stage 1: Project Foundation and Data Models
- [x] Initial repository scaffolding (`open-lecture-bank`).
- [x] Directory structure (`config/`, `docs/`, `src/`, `tests/`, `data/`, `logs/`).
- [x] Core Pydantic v2 data models (`models.py`).
- [x] Configuration loader supporting JSON and `.env` (`config.py`).
- [x] Initial unit tests for models and schemas (`tests/test_models.py`).
- [x] Initial documentation (`ARCHITECTURE.md`, `ROADMAP.md`, `JSON_SCHEMA.md`, `README.md`).

---

## Stage 2: PDF Extraction and Inventory Engine
- [ ] Implement `pdf_extractor.py` using PyMuPDF (`fitz`).
- [ ] Add SHA-256 file hashing to detect duplicate uploads.
- [ ] Extract page-indexed text with slide title and body separation.
- [ ] Implement low-character page detection (< 50 characters) to flag transition or visual-only slides.
- [ ] Implement OCR fallback hook (pytesseract or pdf2image) for scanned documents.
- [ ] Export page-level extraction records to `data/intermediate/extracted/`.

---

## Stage 3: Topic Identification and MCQ Generation
- [ ] Implement `topic_analyzer.py` to identify examinable concepts, key definitions, and formulas.
- [ ] Define modular LLM provider adapter interface (`BaseAIProvider`) in `src/open_lecture_bank/providers/`.
- [ ] Support local heuristic / rule-based generation alongside API adapters (OpenAI, Gemini, Anthropic, Ollama).
- [ ] Enforce the **Four-Option Rule** (exactly options A, B, C, D; single correct answer).
- [ ] Enforce rich explanation generation (both question-level reasoning and option-by-option explanations).

---

## Stage 4: Answer Verification and Question Validation
- [ ] Implement `question_validator.py` with rigorous psychometric checks.
- [ ] Add **Distractor Parity Check**: verify option character length ratios remain below 1.5.
- [ ] Add **Absurdity Filter**: flag and eliminate comical, satirical, or nonsense distractors.
- [ ] Add **Duplicate Detector**: calculate Jaccard word-similarity to detect near-duplicate questions (> 0.65 similarity).
- [ ] Verify source traceability: assert cited page numbers exist within PDF boundaries.

---

## Stage 5: Logical Study Sequencing and JSON Export
- [ ] Implement `study_order.py` to organize topics into 10 pedagogical stages.
- [ ] Model topic prerequisites as a Directed Acyclic Graph (DAG).
- [ ] Implement cycle detection and topological sorting.
- [ ] Implement `exporter.py` to serialize `question_bank.json` and `processing_manifest.json`.
- [ ] Recalculate answer key and difficulty distributions dynamically.

---

## Stage 6: Streamlit User Interface
- [ ] Build interactive web UI (`src/open_lecture_bank/ui/app.py`).
- [ ] Drag-and-drop PDF upload zone.
- [ ] Live progress tracking and batch monitoring.
- [ ] Interactive question bank viewer with search, filtering, and difficulty toggles.
- [ ] One-click export to JSON, CSV, and LMS formats (Moodle XML, QTI, Canvas).

---

## Stage 7: Tests, Documentation, Packaging, and GitHub Release
- [ ] Comprehensive unit and integration test suite with > 85% coverage.
- [ ] Automated CI/CD workflows using GitHub Actions.
- [ ] PyPI package release (`pip install open-lecture-bank`).
- [ ] Public documentation site (MkDocs / Sphinx).
- [ ] Community contributing guidelines and issue templates.
