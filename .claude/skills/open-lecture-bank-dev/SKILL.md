---
name: open-lecture-bank-dev
description: Workflow and quality standards for developing, maintaining, and testing the Open Lecture Bank pipeline and question bank generator.
---

# Open Lecture Bank Development Skill

## Overview

Use this skill when developing, refactoring, extending, or testing features in the `open-lecture-bank` codebase. This skill ensures changes conform to the system's modular architecture, psychometric assessment standards, checkpoint persistence model, and verification requirements.

---

## When to Use This Skill

Activate this skill when:
- Implementing planned pipeline stages from `docs/ROADMAP.md` (PDF extraction, topic analysis, question generation, validation, DAG study ordering, export, or CLI/UI).
- Enhancing or modifying Pydantic models in `src/open_lecture_bank/models.py`.
- Implementing or adjusting validation rules (distractor parity, deduplication, page bounds).
- Designing AI provider adapters or heuristic question generators.
- Writing or maintaining unit and integration tests under `tests/`.

Do **not** use this skill for destructive bulk actions, executing live generation runs against raw user lecture collections without explicit scope, or bypassing documented schemas.

---

## Core Engineering Workflow

### Step 1: Pre-Edit Inspection & Status Mapping
1. Always inspect target modules, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`, and `docs/JSON_SCHEMA.md` before making edits.
2. Determine the exact implementation status of the target feature:
   - **Implemented**: Core data models (`models.py`), settings loader (`config.py`), base serialization (`exporter.py`), validation helpers (`question_validator.py`), DAG cycle check (`study_order.py`).
   - **Scaffolded / Stubs**: Extraction (`pdf_extractor.py`), topic analysis (`topic_analyzer.py`), MCQ generation (`question_generator.py`), pipeline orchestrator (`pipeline.py`), CLI subcommands (`cli.py`).
   - **Planned**: UI (`src/open_lecture_bank/ui/app.py`), provider adapters (`src/open_lecture_bank/providers/`), OCR fallback engine.
3. Identify the smallest useful, testable scope of work. Never attempt multi-stage rewrites in a single change.

### Step 2: Architecture & Contract Adherence
1. **Preserve Data Contracts**: All data structures must validate against Pydantic models in `src/open_lecture_bank/models.py` and match `docs/JSON_SCHEMA.md`.
2. **Subject & Collection Agnostic**: Never hardcode course names, slide numbers, topic names, or file counts. Code must handle arbitrary disciplines (STEM, humanities, medicine) and collection sizes (1 to 100+ PDFs).
3. **Modular Providers**: Decouple generation and analysis logic from specific LLM providers. Maintain provider-agnostic interfaces supporting local heuristics, OpenAI, Gemini, Anthropic, and Ollama.
4. **Durable Checkpoints**:
   - Write intermediate extractions to `data/intermediate/extracted/<sha256>_extracted.json`.
   - Write intermediate batches to `data/intermediate/batches/batch_XX.json`.
   - Support resuming interrupted workflows without repeating finished extraction or generation steps.

### Step 3: Assessment Integrity & Pedagogical Rules
When developing question generation or validation components, strictly enforce:
1. **Four-Option Rule**: Exactly 4 options (`A`, `B`, `C`, `D`), exactly one single correct answer matching `options[correct_option]`.
2. **Distractor Parity & Bias Mitigation**:
   - Option lengths must remain balanced; correct answers must not be conspicuously longer than distractors (length ratio target < 1.5).
   - Distractors must represent plausible domain misconceptions, not comical or impossible assertions.
3. **Answer Key Unpredictability**:
   - Correct answer keys (`A`, `B`, `C`, `D`) must be distributed across items naturally without an easily guessable pattern or forced uniform balance.
4. **Source Traceability & Evidence Grounding**:
   - Every question must populate `source.filename`, `source.pages` (1-indexed, within document page bounds), and `source.evidence` (supporting textual snippet).
   - Structural JSON validity alone is insufficient; answers and explanations must be supported by cited evidence.
5. **Deduplication**: Flag questions exhibiting word-level Jaccard similarity > 0.65.

### Step 4: Incremental Implementation & Testing
1. Implement the minimal required logic to meet the agreed acceptance criteria.
2. Add or update corresponding unit tests in `tests/test_*.py`.
3. Test edge cases: empty strings, single-page documents, invalid option keys, duplicate topics, cyclic prerequisites.
4. Run tests in the appropriate environment and capture actual terminal outputs.
5. **Never fabricate test results, execution logs, or source evidence.** If tests cannot be executed due to environment limitations, clearly report the exact limitation.

### Step 5: Completion Reporting
Every task completion must report:
1. Exact files created, modified, or deleted.
2. Checks performed and actual results obtained (or environment blockers encountered).
3. Current status of the component (e.g., unit tested, scaffolded, integration pending).
4. Explicitly list what remains unimplemented and any migration or integration risks.

---

## Safety & Non-Destructive Rules

- **Zero Data Loss**: Never overwrite, move, or delete files in `data/input/`, `data/output/`, or `data/intermediate/` unless explicitly instructed by the user.
- **No Secret Leakage**: Never hardcode API keys, tokens, or credentials. Use `.env` with fallbacks defined in `.env.example`.
- **Preserve Existing Scaffolding**: Do not delete existing comments, architecture docs, or stubs unless replacing them with tested implementations.
- **No Automatic Academic Claims**: Do not assert that generated questions are academically correct unless evaluated against verified ground truth or source evidence.
