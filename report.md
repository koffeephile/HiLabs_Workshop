# HiLabs Evaluation Framework

## Overview

This project evaluates the reliability of a clinical entity extraction pipeline.

The system processes OCR-generated medical charts and extracts structured medical entities.

Our evaluation framework measures reliability across multiple clinical reasoning dimensions.

---

## Metrics Evaluated

1. Entity Type Error Rate
2. Assertion Error Rate
3. Temporality Error Rate
4. Subject Attribution Error Rate
5. Event Date Accuracy
6. Attribute Completeness

---

## Methodology

The evaluation framework uses rule-based validation using contextual signals.

### Negation Detection

Terms such as:

- no
- denies
- without
- negative for

are used to detect incorrect assertion labeling.

### Temporal Reasoning

Context terms such as:

- history of
- previous
- prior
- scheduled
- upcoming

are used to validate temporality.

### Subject Attribution

Family references such as:

- father
- mother
- family history

are used to detect misattribution between patient and family member.

### Date Validation

Dates extracted via QA metadata are checked against the entity context text.

### Attribute Completeness

Entities containing QA metadata relations are considered to have attribute completeness.

---

## Observed Weaknesses

1. Negation detection errors
2. Temporal reasoning mistakes
3. Family history misclassification
4. Missing attribute metadata

---

## Proposed Reliability Guardrails

1. Negation detection module
2. Temporal reasoning validator
3. Family history classifier
4. Ontology validation using medical knowledge bases
5. Secondary LLM-based validation

---

## Conclusion

The evaluation framework provides a systematic way to detect reliability issues in clinical AI pipelines and highlights areas requiring additional validation layers.