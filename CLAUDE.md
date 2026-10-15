# Claude Repository Guide: Open Lecture Bank

Welcome to the **Open Lecture Bank** repository. This guide provides quick commands, architectural anchors, and workflow pointers for Claude Code.

---

## 1. Development Skill

For active feature implementation, refactoring, or validation audits, use the dedicated development skill:
- **Location**: `.claude/skills/open-lecture-bank-dev/SKILL.md`
- Follow the 5-step engineering workflow: Inspect & Map -> Contract Adherence -> Pedagogical Verification -> Incremental Testing -> Honest Reporting.

For general cross-agent engineering guidelines and architectural baseline, consult `AGENTS.md`.

---

## 2. Common Commands

### Environment Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Running Tests
```bash
# Run entire test suite
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_models.py
pytest tests/test_question_validator.py
pytest tests/test_study_order.py
pytest tests/test_exporter.py
```

### Code Formatting & Quality
```bash
# Code formatting with Black (100 char limit)
black --check src tests
black src tests

# Linting
flake8 src tests
mypy src
```

### CLI Execution
```bash
# Check version and available subcommands
open-lecture-bank --help

# Individual subcommand stubs
open-lecture-bank extract --input ./data/input
open-lecture-bank analyze
open-lecture-bank generate --batch-size 3
open-lecture-bank validate
open-lecture-bank export --output ./data/output
open-lecture-bank run --input ./data/input --output ./data/output
```

---

## 3. Key Architecture & File Map

| Path | Purpose | Current Implementation State |
| :--- | :--- | :--- |
| `src/open_lecture_bank/models.py` | Pydantic v2 data schemas | **Implemented** (MCQ, Topic, Lecture, QuestionBank, Manifest) |
| `src/open_lecture_bank/config.py` | JSON/.env configuration loader | **Implemented** (`AppConfig` & sub-configs) |
| `src/open_lecture_bank/exporter.py` | Output JSON serializers | **Implemented** (`export_question_bank`, `export_manifest`) |
| `src/open_lecture_bank/question_validator.py` | Distractor parity, Jaccard similarity | **Partial** (static audit helpers implemented; bank audit stubbed) |
| `src/open_lecture_bank/study_order.py` | 10-stage DAG sequencer | **Partial** (`verify_cycle_free` implemented; organizer stubbed) |
| `src/open_lecture_bank/pdf_extractor.py` | PyMuPDF text & slide classifier | **Scaffolded** (SHA-256 and directory scanner; extraction stubbed) |
| `src/open_lecture_bank/topic_analyzer.py` | Concept mining & prerequisites | **Planned** (method stubs) |
| `src/open_lecture_bank/question_generator.py` | 4-option MCQ generator | **Planned** (method stubs) |
| `src/open_lecture_bank/pipeline.py` | Pipeline coordinator & checkpoints | **Planned** (method stubs) |
| `src/open_lecture_bank/cli.py` | Click command-line interface | **Scaffolded** (CLI definitions with roadmap notices) |
| `docs/ARCHITECTURE.md` | System design & data flow | Authoritative reference |
| `docs/ROADMAP.md` | 7-stage development plan | Authoritative development milestones |
| `docs/JSON_SCHEMA.md` | Output JSON schema specifications | Authoritative schema contract |

---

## 4. Claude Operational Rules

1. **Always Inspect First**: Never modify code without first inspecting existing functions, types, and schemas.
2. **Never Fabricate**:
   - Never claim tests passed if they were not executed or if the test runner was missing.
   - Never invent source citations, page numbers, or academic facts.
3. **Preserve User Files**: Never modify or delete files under `data/input/`, `data/output/`, or user-provided PDFs.
4. **Follow Pedagogical Rules**:
   - Exactly 4 options (`A`, `B`, `C`, `D`).
   - Single correct answer matching `options[correct_option]`.
   - Distractor length ratio <= 1.5.
   - Realistic distractors based on domain misconceptions.
   - Complete option rationales.
5. **State Unimplemented Work Clearly**: In all completion summaries, distinguish between what is implemented and what remains planned.
