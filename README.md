# nptel-question-bank-generator

> **Universal open-source engine to transform educational lecture slide decks into structured, psychometrically validated MCQ question banks and learning roadmaps.**

[![GitHub Repository](https://img.shields.io/badge/GitHub-mugenkyou%2Fnptel--question--bank--generator-blue?logo=github)](https://github.com/mugenkyou/nptel-question-bank-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](pyproject.toml)
[![Status: Scaffolding](https://img.shields.io/badge/Status-Initial%20Scaffolding%20(WIP)-orange.svg)](docs/ROADMAP.md)

---

## 1. Product Vision

Universities, NPTEL courses, and online educators produce thousands of lecture slide presentations every semester. However, transforming these decks into objective, high-stakes examination questions is a labor-intensive, error-prone manual process.

**Open Lecture Bank** bridges this gap:
- Ingest any directory of lecture PDFs regardless of domain (Engineering, Humanities, Medicine, Science).
- Extract page-indexed slide text while identifying unreadable or visual-only slides.
- Synthesize core examinable topics and extract prerequisite dependencies.
- Generate high-quality multiple-choice questions (MCQs) adhering to strict assessment standards.
- Eliminate distractor giveaways, comical distractors, and option-length cueing.
- Map all topics into a 10-stage prerequisite study sequence modeled as a Directed Acyclic Graph (DAG).
- Export standards-compliant JSON datasets and audit manifests.

> **Note on Implementation Status**: This repository currently contains the initial architecture, data models, configuration, and test scaffolding. Pipeline modules are under active development. See [docs/ROADMAP.md](docs/ROADMAP.md) for progress.

---

## 2. Key Planned Features

- **Universal PDF Ingestion**: Native PyMuPDF integration for digital slides with automated OCR fallback hooks.
- **Strict Four-Option Rule**: Exactly 4 options (`A`, `B`, `C`, `D`), single correct answer, and full rationales for correct and incorrect choices.
- **Psychometric Distractor Parity**: Automated balancing ensuring option character lengths and grammatical structures are parallel, eliminating length-based guessing.
- **Prerequisite-Aware Study Order**: Organizes topics from foundational to advanced in a 10-stage curriculum with strict DAG cycle checking.
- **Provider-Agnostic AI Integration**: Decoupled architecture supporting local rule-based generators or external AI providers (OpenAI, Gemini, Anthropic, Ollama).
- **Persistent Checkpoint Pipeline**: Stateful intermediate batch saving ensuring long courses (60+ lectures) can pause and resume without data loss.

---

## 3. Repository Structure

```
nptel-question-bank-generator/
├── README.md               # Product overview, vision, and usage guide
├── LICENSE                 # Permissive MIT Open Source License
├── pyproject.toml          # PEP 517/518 build and packaging configuration
├── requirements.txt        # Runtime and development dependencies
├── .env.example            # Environment variables template (no secrets)
├── .gitignore              # Ignores venvs, caches, logs, PDFs, and outputs
├── config/
│   └── settings.example.json  # Pipeline thresholds and validation parameters
├── docs/
│   ├── ARCHITECTURE.md     # Modular pipeline design and data flow
│   ├── ROADMAP.md          # 7-stage development plan
│   └── JSON_SCHEMA.md      # Output schemas for question bank and manifest
├── src/
│   └── open_lecture_bank/  # Core package
│       ├── __init__.py     # Package exports and version metadata
│       ├── config.py       # Pydantic settings and config loader
│       ├── models.py       # Core Pydantic v2 data models
│       ├── pdf_extractor.py       # Page-indexed PDF text extractor (planned)
│       ├── topic_analyzer.py      # Topic identification & prerequisites (planned)
│       ├── question_generator.py  # Structured 4-option MCQ generator (planned)
│       ├── question_validator.py  # Parity, duplicate & credibility validator (planned)
│       ├── study_order.py         # 10-stage DAG study order planner (planned)
│       ├── exporter.py            # Question bank & manifest exporter (planned)
│       ├── pipeline.py            # Pipeline coordinator & checkpointing (planned)
│       └── cli.py                 # Command-line entrypoint (planned)
├── tests/                  # Unit and integration test suite
│   ├── test_models.py
│   ├── test_question_validator.py
│   ├── test_study_order.py
│   └── test_exporter.py
├── data/                   # Processing directories (gitignored except .gitkeep)
│   ├── input/              # Drop lecture PDFs here
│   ├── intermediate/       # Persistent checkpoints and batch caches
│   └── output/             # Final question_bank.json and manifest.json
└── logs/                   # Execution and audit logs
```

---

## 4. Proposed Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

```bash
# Clone the repository
git clone https://github.com/mugenkyou/nptel-question-bank-generator.git
cd nptel-question-bank-generator

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies in editable mode
pip install -e .
```

---

## 5. Planned Usage (CLI)

```bash
# Copy example configuration
cp config/settings.example.json config/settings.json
cp .env.example .env

# Place your course lecture PDFs into data/input/
# Run the complete end-to-end pipeline:
open-lecture-bank run --input ./data/input --output ./data/output

# Or run individual modular stages:
open-lecture-bank extract --input ./data/input
open-lecture-bank analyze
open-lecture-bank generate --batch-size 4
open-lecture-bank validate
open-lecture-bank export
```

---

## 6. Contributing & Community

- **Repository**: [https://github.com/mugenkyou/nptel-question-bank-generator](https://github.com/mugenkyou/nptel-question-bank-generator)

Contributions are welcome! Please read [docs/ROADMAP.md](docs/ROADMAP.md) to see current development priorities.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 7. License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
