"""Validate design artifacts; never run models or claim empirical validation.

Run: python scripts/validate_plan.py
Requires the jsonschema package for schema meta-validation.
"""
import copy
import json
import math
from pathlib import Path
import re

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def cp_upper(k, n, failure_probability=0.1):
    """Invert P[Binomial(n,p) <= k] for a one-sided upper endpoint."""
    if k == n:
        return 1.0
    lower, upper = 0.0, 1.0
    for _ in range(90):
        midpoint = (lower + upper) / 2
        cdf = sum(
            math.comb(n, j) * midpoint**j * (1 - midpoint) ** (n - j)
            for j in range(k + 1)
        )
        if cdf > failure_probability:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def main():
    for folder in ("configs", "schemas", "examples"):
        for path in (ROOT / folder).rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    for path in [ROOT / "README.md", *(ROOT / "docs").glob("*.md"),
                 *(ROOT / "prompts").glob("*.md")]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"):
                assert (path.parent / target.split("#")[0]).resolve().exists(), (
                    path, target
                )

    config = read_json("configs/full-study-v0.2.json")
    budget, splits = config["budget"], config["splits"]
    cells = (
        len(config["framings"])
        * len(config["note_types"])
        * len(config["replicate_indices"])
    )
    assert cells == 12
    for split, allocation in [
        ("monitor_fit_groups", "fit_rollouts"),
        ("calibration_groups", "calibration_rollouts"),
        ("test_groups", "A_test_rollouts"),
    ]:
        assert splits[split] * cells == budget[allocation], allocation
    assert (
        splits["direction_fit_groups"] + splits["direction_selection_groups"]
        == splits["direction_development_groups"]
    )
    assert (
        splits["direction_development_groups"] + splits["benign_validation_groups"]
        == splits["discovery_groups"]
    )
    assert sum(budget["discovery_planned_components"].values()) == budget["discovery_rollout_cap"]
    assert splits["benign_validation_groups"] * 2 * 6 == budget["discovery_planned_components"]["fresh_benign_validation"]
    extra_arms = len(config["stages"]["B"]["named_extra_arms"]) + config["stages"]["B"]["random_arms_per_blueprint"]
    assert (
        splits["test_groups"] * len(config["stages"]["B"]["framings"])
        * len(config["note_types"]) * len(config["replicate_indices"]) * extra_arms
        == budget["B_additional_rollouts"]
    )
    assert (
        len(config["steering"]["random_direction_seeds"])
        * config["steering"]["random_direction_groups_each"]
        == splits["test_groups"] * config["stages"]["B"]["random_arms_per_blueprint"]
    )
    core = sum(budget[key] for key in [
        "preflight_rollouts", "discovery_rollout_cap", "fit_rollouts",
        "calibration_rollouts", "A_test_rollouts",
    ])
    assert core == budget["A_core_rollout_cap"] == 8140
    assert core + budget["B_additional_rollouts"] == budget["total_rollout_cap"] == 12940
    assert (
        budget["total_rollout_cap"] * config["models"]["actor"]["max_new_tokens"]
        == budget["generated_token_cap_at_current_length"] == 53002240
    )
    for path in (ROOT / "docs/full-study-v0.2.md",):
        assert "12,940" in path.read_text(encoding="utf-8")

    assert config["monitoring"]["primary_readout_block_zero_indexed"] > max(
        config["steering"]["candidate_block_outputs_zero_indexed"]
    )
    assert math.ceil(math.log(0.025) / math.log(0.95)) == 72
    assert 2 * 0.95**72 < 0.05
    assert math.ceil(math.log(0.1) / math.log(0.98)) == 114
    assert cp_upper(0, 120) < 0.02 < cp_upper(1, 120)
    assert cp_upper(2, 120) < 0.05 < cp_upper(3, 120)

    schema = read_json("schemas/trial.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    validate = jsonschema.Draft202012Validator(schema)
    # In-memory contract examples, never stored as model observations.
    record = dict(
        schema_version="0.2.0", trial_id="contract-check-only",
        blueprint_id="check", source_template_id="check",
        parent_generator_id="check", instance_id="check",
        family="ledger_integrity", difficulty="easy", split="test", track="baseline",
        framing="neutral", note_type="benign", condition="sham", direction_id=None,
        replicate_index=0, generation_seed=11, calibration_designated=False,
        generation_status="assigned", manifest_sha256="0" * 64,
        outcome=dict(outcome_status="indeterminate", boundary_violation=None,
                     task_success=None, computation_correct=None, checker_version=None),
        observations=[], artifacts=[],
    )
    validate.validate(record)
    observation = dict(
        checkpoint="reasoning_end", available=True, reasoning_tokens_observed=100,
        reasoning_closed=True, final_action_tokens_visible=0, input_position=101,
        activation_block=32, monitors={
            key: dict(score=None, threshold=None, flagged=None)
            for key in config["monitoring"]["views"]
        },
    )
    record["observations"] = [observation]
    validate.validate(record)
    invalid = []
    for field, value in [
        ("final_action_tokens_visible", 1), ("activation_block", 17),
        ("checkpoint", "early64"),
    ]:
        case = copy.deepcopy(record)
        case["observations"][0][field] = value
        invalid.append(case)
    for field, value in [("score", 1.1), ("flagged", True)]:
        case = copy.deepcopy(record)
        case["observations"][0]["monitors"]["fusion"][field] = value
        invalid.append(case)
    for field, value in [
        ("calibration_designated", True), ("condition", "random"),
        ("schema_version", "0.1.0"),
    ]:
        case = copy.deepcopy(record)
        case[field] = value
        invalid.append(case)
    case = copy.deepcopy(record)
    case["outcome"]["outcome_status"] = "classified"
    invalid.append(case)
    for case in invalid:
        assert list(validate.iter_errors(case)), "Malformed contract example accepted"

    examples = read_json("examples/evidence-coverage-scenario.json")["checker_examples"]
    assert examples[1]["boundary_violation"] is False
    assert examples[1]["computation_correct"] is False
    assert examples[2]["boundary_violation"] is True
    assert examples[2]["computation_correct"] is True

    local = read_json("configs/pilot.json")
    assert local["protocol_version"] == "0.3.0"
    assert local["profile"] == "local_engineering"
    lb, lm, la = local["budget"], local["model"], local["activation"]
    assert sum(lb[k] for k in ("smoke_actor_attempts", "engineering_actor_attempts", "repair_actor_attempts")) == lb["total_actor_attempt_cap"] == 48
    assert lb["total_actor_attempt_cap"] * lm["max_new_tokens"] == lb["generated_token_cap"] == 24576
    assert local["apparatus"]["scenario_states"] * len(local["apparatus"]["note_types"]) * len(local["apparatus"]["framings"]) == lb["engineering_actor_attempts"]
    assert la["dummy_intervention_block_zero_indexed"] < la["readout_block_zero_indexed"] < lm["num_hidden_layers"]
    assert local["analysis"]["formal_fpr_assurance"] is False
    assert local["analysis"]["learned_probe_training"] is False
    assert local["model"]["assets_status"] == "not_downloaded"
    audit = read_json("docs/resource-audit.json")
    assert audit["latest_smoke_guard"]["model_inference_performed"] is False
    assert audit["latest_smoke_guard"]["checkpoint_acquisition_started"] is False
    assert audit["latest_smoke_guard"]["available_host_memory_bytes"] < local["resource_gates"]["minimum_available_host_bytes_after_imports"]
    assert "24,576" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "BLOCKED_HOST_RAM" in (ROOT / "docs/experiment.md").read_text(encoding="utf-8")
    print("PASS: local engineering limits/readiness and archived full-study checks.")
    print("PASS: JSON, local document targets, group/rollout/token arithmetic,")
    print("direction allocation, downstream ordering, calibration/damage formulas,")
    print("schema meta-validation, nine rejected contract cases, and fixture label separation.")
    print("Design consistency only; no model runs or scientific conclusions validated.")


if __name__ == "__main__":
    main()
