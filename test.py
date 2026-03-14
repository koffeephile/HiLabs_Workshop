import json
import sys
import re
from collections import defaultdict

VALID_ENTITY_TYPES = [
"IMMUNIZATION","MEDICAL_DEVICE","MEDICINE","MENTAL_STATUS",
"PROBLEM","PROCEDURE","SDOH","SOCIAL_HISTORY","TEST","VITAL_NAME"
]

VALID_ASSERTIONS = ["POSITIVE","NEGATIVE","UNCERTAIN"]
VALID_TEMPORALITY = ["CURRENT","CLINICAL_HISTORY","UPCOMING","UNCERTAIN"]
VALID_SUBJECTS = ["PATIENT","FAMILY_MEMBER"]

family_terms = [
"father","mother","brother","sister","grandfather",
"grandmother","family history","mother had","father had"
]

negation_terms = [
"no","denies","denied","without","negative for"
]

history_terms = [
"history of","previous","past","prior"
]

future_terms = [
"scheduled","plan to","next week","upcoming"
]

def compute_rate(errors, counts):
    out = {}
    for k in counts:
        if counts[k] == 0:
            out[k] = 0
        else:
            out[k] = errors.get(k,0) / counts[k]
    return out


def evaluate_entities(entities):

    entity_counts = defaultdict(int)
    entity_errors = defaultdict(int)

    assertion_counts = defaultdict(int)
    assertion_errors = defaultdict(int)

    temporality_counts = defaultdict(int)
    temporality_errors = defaultdict(int)

    subject_counts = defaultdict(int)
    subject_errors = defaultdict(int)

    date_total = 0
    date_correct = 0

    attribute_total = 0
    attribute_present = 0

    for ent in entities:

        entity_text = ent.get("entity","").lower()
        context = ent.get("text","").lower()

        etype = ent.get("entity_type","")
        assertion = ent.get("assertion","")
        temporality = ent.get("temporality","")
        subject = ent.get("subject","")

        # ENTITY TYPE
        if etype in VALID_ENTITY_TYPES:
            entity_counts[etype]+=1
        else:
            entity_counts[etype]+=1
            entity_errors[etype]+=1

        # ASSERTION
        if assertion in VALID_ASSERTIONS:
            assertion_counts[assertion]+=1

            expected = "POSITIVE"
            for n in negation_terms:
                if n in context:
                    expected = "NEGATIVE"

            if assertion != expected:
                assertion_errors[assertion]+=1

        # TEMPORALITY
        if temporality in VALID_TEMPORALITY:
            temporality_counts[temporality]+=1

            expected = "CURRENT"

            for h in history_terms:
                if h in context:
                    expected = "CLINICAL_HISTORY"

            for f in future_terms:
                if f in context:
                    expected = "UPCOMING"

            if temporality != expected:
                temporality_errors[temporality]+=1

        # SUBJECT
        if subject in VALID_SUBJECTS:
            subject_counts[subject]+=1

            expected = "PATIENT"
            for f in family_terms:
                if f in context:
                    expected = "FAMILY_MEMBER"

            if subject != expected:
                subject_errors[subject]+=1

        # EVENT DATE
        qa = ent.get("metadata_from_qa",{})

        if qa and "relations" in qa:

            for rel in qa["relations"]:

                if rel.get("entity_type") in ["exact_date","derived_date"]:
                    date_total+=1
                    date = rel.get("entity","")

                    if date and date in context:
                        date_correct+=1

        # ATTRIBUTE COMPLETENESS
        attribute_total+=1

        if qa and "relations" in qa and len(qa["relations"])>0:
            attribute_present+=1

    results = {}

    results["entity_type_error_rate"] = compute_rate(entity_errors,entity_counts)
    results["assertion_error_rate"] = compute_rate(assertion_errors,assertion_counts)
    results["temporality_error_rate"] = compute_rate(temporality_errors,temporality_counts)
    results["subject_error_rate"] = compute_rate(subject_errors,subject_counts)

    results["event_date_accuracy"] = 0 if date_total==0 else date_correct/date_total
    results["attribute_completeness"] = attribute_present/attribute_total if attribute_total else 0

    return results


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file,"r",encoding="utf-8") as f:
        data = json.load(f)

    entities = data["entities"] if isinstance(data,dict) and "entities" in data else data

    metrics = evaluate_entities(entities)

    output = {
        "file_name": input_file
    }

    output.update(metrics)

    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(output,f,indent=2)


if __name__ == "__main__":
    main()