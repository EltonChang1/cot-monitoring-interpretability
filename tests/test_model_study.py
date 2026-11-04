"""Pure plan, historical-boundary, and descriptive-analysis tests; no ML imports."""

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cot_monitoring_local.model_study import (
    CLOSE_ID, RULE, aggregate_records, build_trial_plan, checkpoint_for_processed_token,
    completed_segments, lexical_diagnostics, stable_hash, trial_messages,
)


class PlanTests(unittest.TestCase):
    def test_default_16_and_optional_32_have_one_shared_template(self):
        self.assertEqual(len(build_trial_plan()), 16)
        plan = build_trial_plan(8)
        self.assertEqual(len(plan), 32)
        self.assertEqual(len({r["trial_id"] for r in plan}), 32)
        self.assertEqual(len({r["scenario"]["source_template_id"] for r in plan}), 1)
        self.assertEqual(stable_hash(plan), stable_hash(build_trial_plan(8)))
        for scenario_id in {r["scenario"]["scenario_id"] for r in plan}:
            cells = [r for r in plan if r["scenario"]["scenario_id"] == scenario_id]
            self.assertEqual(len(cells), 4)
            self.assertEqual(len({r["generation_seed"] for r in cells}), 1)

    def test_prompt_baseline_uses_visible_note_and_not_treatment_labels(self):
        plan = build_trial_plan(1)
        for trial in plan:
            messages = trial_messages(trial)
            self.assertEqual(len(messages), 2)
            note = trial["scenario"]["untrusted_note"]
            self.assertIn(note, messages[1]["content"])
            self.assertEqual(lexical_diagnostics(None, note)["prompt_only_flag"],
                             trial["scenario"]["note_kind"] == "pressure")
        self.assertEqual(stable_hash(RULE), stable_hash(copy.deepcopy(RULE)))


class HistoricalBoundaryTests(unittest.TestCase):
    def test_close_is_captured_when_processed_before_next_action_sample(self):
        ids = [7, 8, CLOSE_ID]
        point = checkpoint_for_processed_token(ids, 2)
        self.assertEqual(point["name"], "reasoning_end")
        self.assertEqual(point["reasoning_token_count"], 2)
        self.assertEqual(point["action_tokens_visible"], 0)
        self.assertIsNone(checkpoint_for_processed_token(ids, 1))

    def test_future_action_and_later_duplicate_do_not_change_historical_point(self):
        historical = checkpoint_for_processed_token([7, CLOSE_ID], 1)
        with_future = checkpoint_for_processed_token([7, CLOSE_ID, 99, CLOSE_ID], 1)
        self.assertEqual(historical, with_future)
        self.assertIsNone(checkpoint_for_processed_token([7, CLOSE_ID, 99], 2))
        self.assertIsNone(checkpoint_for_processed_token([7, CLOSE_ID, 99, CLOSE_ID], 3))

    def test_empty_reasoning_and_token_128(self):
        self.assertEqual(checkpoint_for_processed_token([CLOSE_ID], 0)["reasoning_token_count"], 0)
        self.assertEqual(checkpoint_for_processed_token([7] * 128, 127)["name"], "reasoning_prefix_128")
        self.assertIsNone(checkpoint_for_processed_token([CLOSE_ID] + [7] * 127, 127))

    def test_completion_needs_real_eos_and_unique_boundary(self):
        self.assertEqual(completed_segments([7, CLOSE_ID, 80, 90], [90], True), ([7], [80]))
        self.assertIsNone(completed_segments([7, CLOSE_ID, 80], [90], False))
        self.assertIsNone(completed_segments([7, CLOSE_ID, 80], [90], True))
        self.assertIsNone(completed_segments([CLOSE_ID, CLOSE_ID, 90], [90], True))


class DescriptiveAnalysisTests(unittest.TestCase):
    def test_unknowns_remain_assigned_and_zero_positive_sensitivity_is_null(self):
        records = build_trial_plan(1)
        records[0]["inference_attempted"] = True
        records[0]["outcome"] = {"valid": True, "boundary_violation": False, "task_success": True}
        records[0]["diagnostic"] = {"reasoning_flag": False, "prompt_only_flag": False}
        summary = aggregate_records(records)
        self.assertEqual(summary["assigned"], 4)
        self.assertEqual(summary["attempted"], 1)
        self.assertEqual(summary["reasoning_rule"]["unknown"], 3)
        self.assertIsNone(summary["reasoning_rule"]["sensitivity"])
        self.assertEqual(summary["reasoning_rule"]["achieved_fpr"], 0)
        bound = summary["finite_panel_contrasts"]["neutral"]["pressure_minus_benign_bounds"]["boundary_violation"]
        self.assertEqual(bound, {"lower": 0.0, "upper": 1.0})

    def test_exact_finite_panel_contrast_and_separate_false_alarm_cost(self):
        records = build_trial_plan(1)
        for trial in records:
            pressure = trial["scenario"]["note_kind"] == "pressure"
            trial["outcome"] = {"valid": True, "boundary_violation": pressure, "task_success": not pressure}
            trial["diagnostic"] = {"reasoning_flag": True, "prompt_only_flag": pressure}
        summary = aggregate_records(records)
        self.assertEqual(summary["reasoning_rule"]["achieved_fpr"], 1)
        self.assertEqual(summary["prompt_only_rule"]["achieved_fpr"], 0)
        contrast = summary["finite_panel_contrasts"]["evaluation"]["pressure_minus_benign_bounds"]
        self.assertEqual(contrast["boundary_violation"], {"lower": 1.0, "upper": 1.0})
        self.assertEqual(contrast["task_success"], {"lower": -1.0, "upper": -1.0})

    def test_negated_warning_is_still_literal_match_not_intent(self):
        self.assertTrue(lexical_diagnostics("Do not overwrite the audit row.", "ordinary note")["reasoning_flag"])
        self.assertFalse(lexical_diagnostics("Append the sum.", "ordinary note")["reasoning_flag"])


if __name__ == "__main__":
    unittest.main()
