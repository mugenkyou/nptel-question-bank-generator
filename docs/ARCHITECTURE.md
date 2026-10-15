# Open Lecture Bank: System Architecture

## 1. Architectural Overview

Open Lecture Bank is a modular, extensible, Python-first pipeline designed to ingest arbitrary collections of academic slide decks (PDF format), extract clean page-indexed text, identify examinable concepts, generate psychometrically sound multiple-choice questions (MCQs), validate assessment integrity, and organize knowledge into a prerequisite-aware learning sequence.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           OPEN LECTURE BANK PIPELINE                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
                               ┌───────────────────┐
                               │ 1. PDF Extractor  │
                               │   (PyMuPDF / OCR) │
                               └───────────────────┘
                                         │ Page-indexed JSON
                                         ▼
                               ┌───────────────────┐
                               │ 2. Topic Analyzer │
                               │  (Concept Mining) │
                               └───────────────────┘
                                         │ Topics & Key Concepts
                                         ▼
                               ┌───────────────────┐
                               │ 3. Question Gen   │
                               │ (4-Option Engine) │
                               └───────────────────┘
                                         │ Draft MCQs
                                         ▼
                               ┌───────────────────┐
                               │ 4. Validator      │
                               │ (Parity & Integrity)
                               └───────────────────┘
                                         │ Validated Items
                                         ▼
                               ┌───────────────────┐
                               │ 5. Study Order    │
                               │  (10-Stage DAG)   │
                               └───────────────────┘
                                         │ Global Learning Plan
                                         ▼
                               ┌───────────────────┐
                               │ 6. Exporter       │
                               │ (Bank & Manifest) │
                               └───────────────────┘
```

## 2. Component Responsibilities

| Module | Source Location | Primary Responsibility |
| :--- | :--- | :--- |
| **PDF Extractor** | `src/open_lecture_bank/pdf_extractor.py` | Extracts page-indexed text, counts characters, identifies low-text or transition slides, and detects duplicate files using SHA-256 hashes. |
| **Topic Analyzer** | `src/open_lecture_bank/topic_analyzer.py` | Identifies core examinable topics, extracts key definitions, and deduces pedagogical prerequisite relationships between concepts. |
| **Question Generator** | `src/open_lecture_bank/question_generator.py` | Produces structured, single-answer MCQs with exactly four options (A, B, C, D), plausible distractors, and complete option explanations. |
| **Question Validator** | `src/open_lecture_bank/question_validator.py` | Audits option counts, enforces exact `correct_answer` consistency, checks page reference bounds, eliminates length bias, and detects near-duplicate questions using Jaccard similarity. |
| **Study Order Planner** | `src/open_lecture_bank/study_order.py` | Organizes topics into a 10-stage prerequisite sequence modeled as a strict, cycle-free Directed Acyclic Graph (DAG). |
| **Exporter** | `src/open_lecture_bank/exporter.py` | Serializes consolidated question banks and execution manifests into valid standard JSON formats. |
| **Pipeline Coordinator** | `src/open_lecture_bank/pipeline.py` | Coordinates execution across stages, writes persistent checkpoints to disk, and allows paused workflows to resume seamlessly. |
| **Data Models** | `src/open_lecture_bank/models.py` | Pydantic v2 schemas providing type safety and validation across all pipeline entities. |
| **CLI** | `src/open_lecture_bank/cli.py` | Command-line interface offering subcommands (`extract`, `analyze`, `generate`, `validate`, `export`, `run`). |

## 3. Data Flow & Checkpoint Persistence

To handle courses with 50 to 100+ lecture decks without risking context window overflow or process failure:

1. **Extraction Checkpoints (`data/intermediate/extracted/`)**:
   - Each input PDF is processed independently and saved as `<hash>_extracted.json`.
   - If processing is interrupted, existing files are loaded from disk without re-extracting.
2. **Batch Generation Checkpoints (`data/intermediate/batches/`)**:
   - Questions are generated in configurable batches (default: 3 to 5 lectures per batch).
   - Intermediate outputs are written to `batch_XX.json`.
3. **Consolidation**:
   - The Exporter reads validated batches, updates global indices, recalculates distribution metrics, and outputs the final deliverables in `data/output/`.

## 4. Psychometric Integrity & Distractor Balancing

Standard automated question generation often produces two critical flaws:
1. **Comical / Absurd Distractors**: Distractors that are obviously impossible or nonsensical.
2. **Option-Length Cueing**: Correct answers that are 2x to 5x longer and more qualified than distractors.

Open Lecture Bank's `QuestionValidator` and `QuestionGenerator` enforce:
- **Parallel Syntactic Structure**: All options (A, B, C, D) are matched in grammatical structure and character length.
- **Plausibility Checking**: Distractors must reflect plausible misconceptions, incorrect formula applications, or related domain terminology.
- **Answer Key Balance**: Correct answer positions are evenly distributed across keys A, B, C, and D (~25% each).

## 5. Universal & Subject-Agnostic Design

Open Lecture Bank does not hardcode any subject matter, course name, or fixed file count. It dynamically adapts to:
- Natural Sciences (Physics, Chemistry, Earth Sciences, Biology)
- Engineering (Civil, Mechanical, Computer Science, Electrical)
- Humanities, Management, and Social Sciences
- Arbitrary lecture counts (from a single 10-slide seminar to an 80-lecture semester course).
