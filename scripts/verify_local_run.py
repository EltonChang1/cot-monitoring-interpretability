"""Verify completed local-study artifacts without running a model."""
import argparse
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from cot_monitoring_local import build_scenarios, check_action
from cot_monitoring_local.model_study import (
    RULE, CLOSE_ID, aggregate_records, completed_segments, lexical_diagnostics, stable_hash,
)

def verify(run_dir):
    run = Path(run_dir)
    report = json.loads((run/"progress.json").read_text(encoding="utf-8"))
    assignment = json.loads((run/"assigned-plan.json").read_text(encoding="utf-8"))
    assert report["status"]=="completed_finite_panel", report["status"]
    assert stable_hash(assignment["plan"])==assignment["sha256"]==report["plan_sha256"]
    assert stable_hash(report["rule"])==report["rule_sha256"]==stable_hash(RULE)
    assert report["summary"]==aggregate_records(report["trials"])
    assert len(report["trials"])==len(assignment["plan"])
    expected = {x["trial_id"]:x for x in assignment["plan"]}
    assert len(expected)==len(report["trials"])
    count=0
    for trial in report["trials"]:
        original=expected[trial["trial_id"]]
        for key in ("scenario","framing","generation_seed"):
            assert trial[key]==original[key], (trial["trial_id"],key)
        assert trial["inference_attempted"] is True
        ids=trial["generated_token_ids"]
        assert trial["generated_tokens"]==len(ids)<=report["sampling"]["max_new_tokens"]
        for checkpoint in trial.get("checkpoints",{}).values():
            index=checkpoint["processed_generated_index"]
            prefix=ids[:index+1]
            assert checkpoint["action_tokens_visible"]==0
            assert checkpoint["block_zero_indexed"]==20
            assert checkpoint["hidden_width"]==1024
            assert checkpoint["all_finite"] is True
            assert len(checkpoint["vector"])==1024
            assert all(math.isfinite(x) for x in checkpoint["vector"])
            assert math.isclose(math.sqrt(sum(x*x for x in checkpoint["vector"])),
                                checkpoint["l2_norm"], rel_tol=1e-5, abs_tol=1e-4)
            if checkpoint["name"]=="reasoning_end":
                assert ids[index]==CLOSE_ID and prefix.count(CLOSE_ID)==1
                assert checkpoint["reasoning_token_count"]==index
                count+=1
            else:
                assert checkpoint["name"]=="reasoning_prefix_128"
                assert len(prefix)==128 and CLOSE_ID not in prefix
        if "action_text" in trial:
            scenario=next(s for s in build_scenarios(8) if s.scenario_id==trial["scenario"]["scenario_id"])
            assert asdict(check_action(scenario,trial["action_text"]))==trial["outcome"]
            assert trial["completion_ended"]
        if not trial["outcome"]["valid"]:
            assert trial["outcome"]["boundary_violation"] is None
            assert trial["outcome"]["task_success"] is None
        if trial["diagnostic"]["reasoning_flag"] is not None:
            assert "reasoning_end" in trial["checkpoints"]
            assert lexical_diagnostics(trial["reasoning_text"],trial["scenario"]["untrusted_note"])==trial["diagnostic"]
        assert json.loads((run/(trial["trial_id"]+".json")).read_text(encoding="utf-8"))==trial
    assert count==report["summary"]["reasoning_end_readouts"]
    for name,key in (("model_study.py","worker_source_sha256"),("simulator.py","checker_source_sha256")):
        assert hashlib.sha256((ROOT/"src/cot_monitoring_local"/name).read_bytes()).hexdigest()==report[key], key
    return report, {"status":"verified","assigned_trials":len(report["trials"]),
                    "verified_pre_action_readouts":count,
                    "plan_rule_source_hashes_match":True,"outcomes_and_aggregates_recomputed":True,
                    "scope":"Artifact/index verification; activations are not recomputed."}

def verify_token_text(report):
    os.environ.setdefault("USE_TF", "0")
    os.environ.setdefault("USE_FLAX", "0")
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        report["model_id"], revision=report["model_revision"],
        cache_dir=str(Path.home()/".cache/cot-monitoring-interpretability/huggingface"),
        local_files_only=True, token=False, trust_remote_code=False,
    )
    reasoning_count = action_count = 0
    for trial in report["trials"]:
        ids = trial["generated_token_ids"]
        assert tokenizer.decode(ids, skip_special_tokens=False) == trial["raw_generated_text"]
        if "reasoning_text" in trial:
            assert tokenizer.decode(ids[:ids.index(CLOSE_ID)], skip_special_tokens=False) == trial["reasoning_text"]
            reasoning_count += 1
        if "action_text" in trial:
            assert tokenizer.decode(ids[ids.index(CLOSE_ID)+1:-1], skip_special_tokens=False).strip() == trial["action_text"]
            action_count += 1
    return {"raw_generation_trials":len(report["trials"]), "reasoning_slices":reasoning_count,
            "action_slices":action_count, "model_forward_calls":0}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir",required=True)
    parser.add_argument("--output")
    parser.add_argument("--verify-token-text", action="store_true")
    args=parser.parse_args()
    report,result=verify(args.run_dir)
    if args.verify_token_text:
        result["cached_tokenizer_verification"] = verify_token_text(report)
    if args.output:
        target=Path(args.output)
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open("x",encoding="utf-8") as out:
            out.write(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
