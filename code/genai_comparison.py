"""Pre-register and run a separate 30-response aggregate prompt comparison."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import random

import genai

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "genai" / "run_03"
REPETITIONS = 5
CRITERIA = {
    "numerical_accuracy": "Pass if every numerical claim matches the context or a correctly rounded derivation; omission alone is not an error. Fail for wrong values, denominators or metric meanings.",
    "complete_denominators": "Pass only if both detected bad cases out of all actual bad cases AND falsely flagged good cases out of all actual good cases are explicitly stated with correct counts and denominators. Percentages alone do not pass.",
    "both_errors": "Pass if both bad cases predicted good and good cases predicted bad are described unambiguously. Correct false-approval/false-rejection labels with counts suffice. Merely listing metrics does not.",
    "bounded_claims": "Pass if the answer explicitly limits the example to historical/teaching or synthetic evidence AND makes no unsupported causal, default-probability, actual-profit, fairness or deployment claim. Conditional illustrative costs are allowed; recommendations to approve/reject loans or deploy are not. Generalizations beyond the evidence fail even with a disclaimer.",
    "word_limit": "Automatic pass for 120-180 whitespace-separated words inclusive, including headings and Markdown tokens. Otherwise fail. This is length compliance, not a measure of clarity.",
}


def count_metrics(tn, fp, fn, tp):
    """Derive all synthetic metrics from counts; AUC needs scores and is omitted."""
    if any(type(value) is not int or value < 0 for value in (tn, fp, fn, tp)):
        raise ValueError("Counts must be nonnegative integers.")
    good, bad = tn + fp, tp + fn
    if not good or not bad:
        raise ValueError("Both actual classes must be present.")
    return {
        "accuracy": (tn + tp) / (good + bad),
        "balanced_accuracy": (tn / good + tp / bad) / 2,
        "bad_precision": tp / (tp + fp) if tp + fp else 0,
        "bad_recall": tp / bad,
        "bad_f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0,
        "cost_per_case": (5 * fn + fp) / (good + bad),
        "true_good": tn, "false_rejections": fp,
        "false_approvals": fn, "true_bad": tp,
    }


def scenarios():
    actual = genai.experiment_context()
    actual["evidence_type"] = "Actual saved project test results; not newly evaluated."
    result = {"actual_results": actual}
    for name, counts in {
        "high_accuracy_low_detection": (176, 4, 16, 4),
        "high_detection_many_false_flags": (45, 55, 10, 90),
    }.items():
        tn, fp, fn, tp = counts
        context = {
            "evidence_type": "SYNTHETIC arithmetic test scenario, not observed project results or a fitted model.",
            "dataset": "Invented aggregate counts for testing an explanation; no applicant records.",
            "model": "Fictional classifier; no model was trained for this scenario.",
            "test_cases": sum(counts),
            "actual_good_risks": tn + fp, "actual_bad_risks": fn + tp,
            "test_metrics": count_metrics(*counts),
            "always_good_reference": count_metrics(tn + fp, 0, fn + tp, 0),
            "error_definitions": actual["error_definitions"],
            "cost_assumption": actual["cost_assumption"],
            "limits": "Synthetic teaching example only. No future default probabilities, fairness, profit or present-day lending suitability demonstrated. AUC is not available.",
        }
        result[name] = context
    return result


def fingerprints():
    paths = [Path(__file__), ROOT / "code/genai.py", ROOT / "results/final_test.json",
             *genai.PROMPT_PATHS.values()]
    # Normalize text line endings so Git's Windows checkout does not invalidate the protocol.
    return {path.relative_to(ROOT).as_posix():
            sha256(path.read_text(encoding="utf-8").encode()).hexdigest() for path in paths}


def prepare(output=OUTPUT):
    """Write the full protocol before requesting any responses; never overwrite."""
    output = Path(output)
    contexts = scenarios()
    rng = random.Random(42)
    blocks = [(name, repetition) for name in contexts
              for repetition in range(1, REPETITIONS + 1)]
    rng.shuffle(blocks)
    order = []
    for name, repetition in blocks:
        variants = ["simple", "structured"]
        rng.shuffle(variants)
        order.extend({"scenario": name, "repetition": repetition, "variant": variant}
                     for variant in variants)
    protocol = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "question": "How consistently do two unchanged prompts explain counts, both errors and limits across three aggregate scenarios?",
        "relationship_to_pilot": "Prospective extension after inspecting the original six answers; pilot results are not pooled. No claim of an independent confirmatory study.",
        "model": genai.MODEL, "instructions": genai.COMMON_INSTRUCTIONS,
        "settings": {"temperature": .7, "reasoning_effort": "none", "max_output_tokens": 800,
                     "store": False, "max_retries": 0},
        "repetitions_per_variant_per_scenario": REPETITIONS,
        "planned_requests": len(order), "request_order_seed": 42,
        "order_note": "Shuffled scenario/repetition blocks, randomized prompt order within each block. API generation itself is not seeded.",
        "order": order, "contexts": contexts,
        "prompts": {name: {variant: genai.request_text(variant, context)
                           for variant in genai.PROMPT_PATHS}
                    for name, context in contexts.items()},
        "source_fingerprints": fingerprints(), "criteria": CRITERIA,
        "review_method": "Deterministic word counts plus AI-assisted reading of every response against its context, with evidence excerpts. Not blinded or independent. Human sign-off pending. No extra API grading requests.",
        "analysis_plan": "Report criterion pass counts by scenario and prompt, plus totals out of 15 per prompt. No composite score or significance claim. Preserve every attempt, including incomplete/failed responses. Stop on the first failed/incomplete request; no automatic retry or replacement.",
        "limits": "Only three purposefully selected scenarios, one model and five responses per cell. Two scenarios are synthetic; wording, class balance and error patterns vary together. Prompts differ in several instructions, and their requested criteria partly overlap the evaluation. Repetitions are not independent task samples. This tests prompt compliance, not ML prediction performance or general model quality.",
        "pricing_reference": "https://developers.openai.com/api/docs/models/gpt-5.4-mini",
        "estimated_cost_rates_usd_per_million": {"input": .75, "cached_input": .075, "output": 4.5},
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output / "protocol.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(protocol, indent=2) + "\n")
    return protocol


def run(output=OUTPUT):
    """Execute only the frozen plan, sequentially, with a fresh request per trial."""
    output = Path(output)
    protocol = json.loads((output / "protocol.json").read_text(encoding="utf-8"))
    if (output / "attempts.jsonl").exists():
        raise FileExistsError("Attempts already exist; do not overwrite or silently resume.")
    if protocol["source_fingerprints"] != fingerprints():
        raise ValueError("Protocol sources changed after preparation.")
    if not genai.get_api_key():
        raise ValueError("Configure the local API key first.")
    with (output / "attempts.jsonl").open("x", encoding="utf-8", buffering=1) as stream:
        for index, trial in enumerate(protocol["order"], start=1):
            try:
                record = genai.generate_explanation(
                    trial["variant"], context=protocol["contexts"][trial["scenario"]])
            except Exception as error:
                record = {"status": "request_failed", "error_type": type(error).__name__}
            record.update(trial, attempt=index)
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"Attempt {index}/{protocol['planned_requests']}: "
                  f"{trial['scenario']}, {trial['variant']}, {record['status']}", flush=True)
            if record["status"] != "completed" or not record.get("output_text", "").strip():
                break


def export_outputs(output=OUTPUT):
    """Readable, unedited answers and objective length checks; no API requests."""
    output = Path(output)
    records = [json.loads(line) for line in (output / "attempts.jsonl").read_text(encoding="utf-8").splitlines()]
    lines = ["# Expanded comparison: all recorded answers", "",
             "Actual results and explicitly synthetic scenarios are separate. Raw text is unchanged.",
             "Word counts use whitespace-separated tokens; they do not measure clarity.", ""]
    for record in records:
        lines.extend([f"## Attempt {record['attempt']}: {record['scenario']} / {record['variant']}", "",
                      f"Repetition {record['repetition']} of 5. Status: {record['status']}.", ""])
        if record.get("output_text"):
            words = len(record["output_text"].split())
            lines.extend([f"Word count: {words}; within 120-180: {120 <= words <= 180}.", "",
                          record["output_text"], ""])
    (output / "outputs.md").write_text("\n".join(lines), encoding="utf-8")
    return records


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run", "export"])
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    {"prepare": prepare, "run": run, "export": export_outputs}[args.action](args.output_dir)
