"""Explain saved aggregate results or an explicitly submitted fictional profile."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import time
import tomllib

from openai import OpenAI


def explanation_error_message(error):
    """Return actionable fixed text without displaying provider bodies or keys."""
    name = type(error).__name__
    if isinstance(error, TypeError) and "unexpected keyword argument 'context'" in str(error):
        return "The app has an older explanation module loaded. Restart the local Streamlit server and try again."
    if name == "AuthenticationError":
        return "OpenAI rejected the API key. Check the secret key in the local configuration."
    if name == "PermissionDeniedError":
        return "This OpenAI project does not have permission to use the selected model."
    if name == "RateLimitError":
        if getattr(error, "code", None) in {
            "insufficient_quota", "billing_hard_limit_reached", "organization_spend_limit_exceeded",
            "project_spend_limit_exceeded", "organization_usage_limit_exceeded",
        }:
            return "The OpenAI account has reached a credit, billing or spending limit. Check the API project's billing settings before retrying."
        return "OpenAI is temporarily limiting requests. Wait before trying again."
    if name == "APITimeoutError":
        return "The OpenAI request timed out. Try again later; the risk prediction is unchanged."
    if name == "APIConnectionError":
        return "The app could not connect to OpenAI. Check the connection and try again."
    return "The AI explanation is unavailable. The risk prediction still works; use the calculated contributions or recorded examples."

ROOT = Path(__file__).resolve().parents[1]
MODEL = "gpt-5.4-mini-2026-03-17"
MAX_OUTPUT_TOKENS = 800
COMMON_INSTRUCTIONS = (
    "Write in English for a bank manager without a machine-learning background. "
    "Use 120-180 words."
)
PROMPT_PATHS = {name: ROOT / "prompts" / f"explanation_{name}.txt"
                for name in ["simple", "structured"]}


def get_api_key():
    """Read only explicit local configuration, never print or store the key."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        path = ROOT / ".streamlit" / "secrets.toml"
        if path.exists():
            settings = tomllib.loads(path.read_text(encoding="utf-8-sig"))
            key = str(settings.get("OPENAI_API_KEY", "")).strip()
    return key


def experiment_context():
    """Allowlist aggregate facts; no raw rows, input profiles or credentials."""
    report = json.loads((ROOT / "results" / "final_test.json").read_text(encoding="utf-8"))
    scores = report["selected_model_metrics"]
    return {
        "dataset": "UCI Statlog German Credit Data, historical teaching dataset",
        "model": "Logistic regression, balanced class weights, seven inputs, score threshold 0.5",
        "training_cases": report["training_cases"], "test_cases": report["test_cases"],
        "actual_good_risks": scores["true_good"] + scores["false_rejections"],
        "actual_bad_risks": scores["true_bad"] + scores["false_approvals"],
        "test_metrics": scores,
        "always_good_reference": report["always_good_reference_metrics"],
        "error_definitions": {"false_approval": "bad risk predicted good",
                              "false_rejection": "good risk predicted bad"},
        "cost_assumption": "5 per false approval, 1 per false rejection, 0 if correct; illustrative units, not currency",
        "limits": "Historical labels; scores not calibrated default probabilities; no fairness or present-day lending suitability demonstrated.",
    }


def request_text(variant, context=None):
    path = ROOT / "prompts" / "explanation_profile.txt" if variant == "profile" else PROMPT_PATHS[variant]
    if variant == "profile" and context is None:
        raise ValueError("A profile explanation requires the submitted profile and model contributions.")
    prompt = path.read_text(encoding="utf-8").strip()
    facts = experiment_context() if context is None else context
    return prompt + "\n\nRESULTS (JSON):\n" + json.dumps(facts, indent=2)


def generate_explanation(variant="structured", *, context=None, api_key=None, client=None):
    """One request, no tools or retries; return exact prompt/output and usage."""
    prompt = request_text(variant, context)
    if client is None:
        key = get_api_key() if api_key is None else api_key
        if not key:
            raise ValueError("Configure OPENAI_API_KEY locally before requesting a live explanation.")
        if not key.startswith("sk-"):
            raise ValueError("Use the secret API key starting with sk-, not its management identifier.")
        client = OpenAI(api_key=key, base_url="https://api.openai.com/v1", timeout=40, max_retries=0)
    started = time.monotonic()
    response = client.responses.create(
        model=MODEL, instructions=COMMON_INSTRUCTIONS, input=prompt,
        reasoning={"effort": "none"}, temperature=.7,
        max_output_tokens=MAX_OUTPUT_TOKENS, store=False,
    )
    elapsed = time.monotonic() - started
    usage = response.usage.model_dump() if response.usage is not None else None
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "variant": variant, "requested_model": MODEL, "returned_model": response.model,
        "response_id": response.id, "status": response.status,
        "instructions": COMMON_INSTRUCTIONS, "prompt": prompt,
        "settings": {"reasoning_effort": "none", "temperature": .7,
                     "max_output_tokens": MAX_OUTPUT_TOKENS, "store": False, "max_retries": 0},
        "output_text": response.output_text, "usage": usage,
        "elapsed_seconds": round(elapsed, 3),
        "final_report_sha256": sha256((ROOT / "results" / "final_test.json").read_bytes()).hexdigest(),
    }


def run_experiment(output_dir=None):
    """Six calls in paired order. Save every attempt; never silently cherry-pick."""
    output = ROOT / "results" / "genai" if output_dir is None else Path(output_dir)
    if (output / "attempts.jsonl").exists():
        raise FileExistsError("Experiment attempts already exist. Review them; do not overwrite the experiment.")
    if not get_api_key():
        raise ValueError("Configure OPENAI_API_KEY locally first.")
    output.mkdir(parents=True, exist_ok=True)
    protocol = {
        "question": "Can generative AI explain credit-scoring results clearly without unsupported claims?",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL, "repetitions_per_variant": 3,
        "order": ["simple", "structured"] * 3,
        "instructions": COMMON_INSTRUCTIONS,
        "prompts": {name: request_text(name) for name in PROMPT_PATHS},
        "settings": {"temperature": .7, "reasoning_effort": "none", "max_output_tokens": MAX_OUTPUT_TOKENS},
        "criteria": {
            "numerical_accuracy": "0: wrong number/denominator; 1: no numeric error but key counts omitted; 2: correct 46/60 detected and 40/140 falsely flagged, with no numeric errors.",
            "clarity": "0: hard to follow; 1: understandable with unexplained jargon or outside 120-180 words; 2: clear for a nontechnical reader and 120-180 words.",
            "balanced_errors": "0: neither error type explained; 1: one type explained; 2: explains both bad predicted good and good predicted bad.",
            "unsupported_claims": "0: invented cause, default probability, actual savings/profit or deployment recommendation; 1: none of those, but historical scope or need for caution omitted; 2: no unsupported claim and historical/teaching limits clearly stated.",
        },
        "review_method": "AI-assisted qualitative review of every raw output with quoted evidence; human sign-off pending. No independent or blinded raters.",
        "limits": "Six outputs on one fixed results summary; prompt versions differ in multiple instructions. Descriptive comparison, not a statistical test or proof of general model quality.",
    }
    with (output / "protocol.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(protocol, indent=2) + "\n")
    with (output / "attempts.jsonl").open("x", encoding="utf-8", buffering=1) as stream:
        for index, variant in enumerate(protocol["order"], start=1):
            try:
                record = generate_explanation(variant)
            except Exception as error:
                # Never serialize provider error bodies, headers or credentials.
                record = {"variant": variant, "status": "request_failed",
                          "error_type": type(error).__name__}
            record["attempt"] = index
            record["repetition"] = (index + 1) // 2
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"Attempt {index}/6: {variant}, {record['status']}")
            if record["status"] == "request_failed":
                break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Use a new folder for a separately documented repair run.")
    run_experiment(parser.parse_args().output_dir)
