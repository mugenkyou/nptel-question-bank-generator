# Open Lecture Bank: JSON Output Schemas

Open Lecture Bank produces two primary standardized deliverables upon completion:
1. `question_bank.json`: Consolidated assessment items, topics, and prerequisite learning order.
2. `processing_manifest.json`: Operational record of all files processed, page audits, and limitations.

---

## 1. Consolidated Question Bank Schema (`question_bank.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "QuestionBank",
  "type": "object",
  "required": ["metadata", "lectures", "global_topic_index", "prerequisite_study_sequence", "review_required"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["title", "schema_version", "expected_pdf_count", "processed_pdf_count", "total_topics", "total_questions"],
      "properties": {
        "title": { "type": "string" },
        "course_title": { "type": "string" },
        "instructor": { "type": "string" },
        "schema_version": { "type": "string", "example": "2.0-audited" },
        "expected_pdf_count": { "type": "integer" },
        "processed_pdf_count": { "type": "integer" },
        "complete_pdf_count": { "type": "integer" },
        "incomplete_pdf_count": { "type": "integer" },
        "failed_pdf_count": { "type": "integer" },
        "missing_source_files": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "filename": { "type": "string" },
              "status": { "type": "string" },
              "explanation": { "type": "string" }
            }
          }
        },
        "total_topics": { "type": "integer" },
        "total_questions": { "type": "integer" },
        "difficulty_distribution": {
          "type": "object",
          "properties": {
            "easy": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } },
            "medium": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } },
            "hard": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } }
          }
        },
        "answer_key_distribution": {
          "type": "object",
          "properties": {
            "A": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } },
            "B": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } },
            "C": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } },
            "D": { "type": "object", "properties": { "count": { "type": "integer" }, "percentage": { "type": "number" } } }
          }
        }
      }
    },
    "lectures": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["lecture_id", "source_file", "processing_status", "total_pages", "topics"],
        "properties": {
          "lecture_id": { "type": "string", "example": "L001" },
          "source_file": { "type": "string", "example": "Lecture_01.pdf" },
          "processing_status": { "type": "string", "enum": ["complete", "partial", "failed"] },
          "total_pages": { "type": "integer" },
          "pages_inspected": { "type": "array", "items": { "type": "integer" } },
          "topics": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["topic_id", "topic_name", "importance", "questions"],
              "properties": {
                "topic_id": { "type": "string", "example": "L001-T001" },
                "topic_name": { "type": "string" },
                "importance": { "type": "string", "enum": ["high", "medium", "low"] },
                "key_concepts": { "type": "array", "items": { "type": "string" } },
                "questions": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["question_id", "question_type", "difficulty", "question", "options", "correct_option", "correct_answer", "explanation", "source"],
                    "properties": {
                      "question_id": { "type": "string", "example": "L001-T001-Q001" },
                      "question_type": { "type": "string", "enum": ["conceptual", "definition", "application", "comparison", "procedure", "formula", "numerical"] },
                      "difficulty": { "type": "string", "enum": ["easy", "medium", "hard"] },
                      "question": { "type": "string" },
                      "options": {
                        "type": "object",
                        "required": ["A", "B", "C", "D"],
                        "properties": {
                          "A": { "type": "string" },
                          "B": { "type": "string" },
                          "C": { "type": "string" },
                          "D": { "type": "string" }
                        }
                      },
                      "correct_option": { "type": "string", "enum": ["A", "B", "C", "D"] },
                      "correct_answer": { "type": "string" },
                      "explanation": { "type": "string" },
                      "option_explanations": {
                        "type": "object",
                        "properties": {
                          "A": { "type": "string" },
                          "B": { "type": "string" },
                          "C": { "type": "string" },
                          "D": { "type": "string" }
                        }
                      },
                      "source": {
                        "type": "object",
                        "required": ["filename", "pages", "evidence"],
                        "properties": {
                          "filename": { "type": "string" },
                          "pages": { "type": "array", "items": { "type": "integer" } },
                          "evidence": { "type": "string" }
                        }
                      },
                      "verification_status": { "type": "string", "enum": ["verified", "review_required"] }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "global_topic_index": { "type": "array" },
    "prerequisite_study_sequence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["sequence_number", "topic_id", "canonical_topic_name", "recommended_stage", "prerequisite_topic_ids", "learning_objectives"],
        "properties": {
          "sequence_number": { "type": "integer" },
          "topic_id": { "type": "string" },
          "lecture_id": { "type": "string" },
          "source_file": { "type": "string" },
          "canonical_topic_name": { "type": "string" },
          "recommended_stage": { "type": "string" },
          "prerequisite_topic_ids": { "type": "array", "items": { "type": "string" } },
          "learning_objectives": { "type": "array", "items": { "type": "string" } },
          "associated_question_ids": { "type": "array", "items": { "type": "string" } },
          "pedagogical_rationale": { "type": "string" }
        }
      }
    },
    "review_required": { "type": "array" }
  }
}
```
