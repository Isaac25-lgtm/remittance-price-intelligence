"""Post-freeze descriptive measurement and explicit, non-empirical linkage scenarios."""
import csv
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def era(q):
    if q < 2021 * 4:
        return "before_target_2021Q2"
    if q == 2021 * 4:
        return "transition_target_2021Q2"
    if q < 2022 * 4 + 2:
        return "between_classification_transitions"
    if q == 2022 * 4 + 2:
        return "transition_target_2022Q4"
    return "after_target_2022Q4"


def funding(value):
    if not value:
        return "missing"
    if "," in value:
        return "combined_instruments"
    if "card" in value:
        return "card"
    if "bank" in value:
        return "bank_transfer"
    if "mobile" in value:
        return "mobile_money"
    if "cash" in value:
        return "cash"
    return "other"


def payout(value):
    if not value:
        return "missing"
    if "," in value:
        return "combined_methods"
    if "bank" in value or "account" in value:
        return "bank_account"
    if "wallet" in value or "mobile" in value:
        return "mobile_wallet"
    if "cash" in value:
        return "cash"
    return "other"


def adversarial_false_positive(n, stays, failures, invalid_links):
    """Assumed false-positive links become unknown; denominator remains all origins."""
    valid = stays + failures
    if not 0 <= invalid_links <= valid <= n:
        raise ValueError("Invalid sensitivity counts")
    # Remove either as many observed stays or as many observed failures as possible.
    min_stays = stays - min(stays, invalid_links)
    max_stays = stays - max(0, invalid_links - failures)
    remaining = valid - invalid_links
    min_failures = failures - min(failures, invalid_links)
    return dict(n_eligible=n, assumed_false_positive_links=invalid_links, retained_valid=remaining,
                unknown=n-remaining, conditional_min=min_stays/remaining if remaining else None,
                conditional_max=max_stays/remaining if remaining else None,
                all_origin_lower=min_stays/n, all_origin_upper=1-min_failures/n)


def main():
    review = load_module("autonomous_review", HERE / "review.py")
    review.verify_freeze()
    if not (review.PRIVATE / "unblinding_event.json").exists():
        raise ValueError("Post-freeze unblinding checkpoint required")
    m = load_module("independent_measurement", ROOT / "research_completion/phase3/code/measurement.py")
    records = m.load_source()
    core, _, _, _ = m.construct(records, basket=0, threshold=3, strict=False)
    strict, _, _, _ = m.construct(records, basket=0, threshold=3, strict=True)
    assert m.estimate(core, "core")["n_eligible"] == 45343
    assert core.valid.sum() == 36429 and core.stay.sum() == 29546 and core.unknown.sum() == 8914
    assert strict.valid.sum() == 30570 and strict.stay.sum() == 24776 and strict.unknown.sum() == 14773
    assert core.private_index.tolist() == strict.private_index.tolist()
    for frame in [core, strict]:
        frame["source_era"] = frame.qidx.map(era)
        frame["funding_group"] = frame.private_index.map(lambda i: funding(records[i][1][2]))
        frame["payout_group"] = frame.private_index.map(lambda i: payout(records[i][1][4]))
    rows = []
    support = []
    for label, frame in [("core", core), ("strict", strict)]:
        for field in ["source_era", "region", "provider_type", "funding_group", "payout_group"]:
            for group, sub in frame.groupby(field):
                support.append(dict(identity_rule=label, group_field=field, group=group, n_eligible=len(sub),
                                    reported=len(sub) >= 30, minimum_reported_n=30))
                if len(sub) >= 30:
                    rows.append(dict(group_field=field, group=group, **m.estimate(sub, label)))
    m.pd.DataFrame(rows).to_csv(HERE / "MEASUREMENT_GROUP_SENSITIVITIES.csv", index=False)
    m.pd.DataFrame(support).to_csv(HERE / "GROUP_SUPPORT.csv", index=False)
    paired = []
    for field in ["source_era", "region", "provider_type", "funding_group", "payout_group"]:
        for group, sub in core.groupby(field):
            if len(sub) < 30:
                continue
            indices = sub.index
            # New strict unknowns are exactly the core-valid rows excluded by strict.
            changed = sub[(sub.valid == 1) & (strict.loc[indices, "valid"] == 0)]
            unchanged = sub[(sub.valid == 1) & (strict.loc[indices, "valid"] == 1)]
            paired.append(dict(group_field=field, group=group, n_eligible=len(sub), core_valid=int(sub.valid.sum()),
                strict_valid=int(strict.loc[indices, "valid"].sum()), newly_unknown=len(changed),
                changed_core_stay=int(changed.stay.sum()), changed_core_fail=int(changed.fail.sum()),
                changed_core_continuity=changed.stay.mean() if len(changed) else None,
                unchanged_core_continuity=unchanged.stay.mean() if len(unchanged) else None,
                width_difference=len(changed)/len(sub)))
    m.pd.DataFrame(paired).to_csv(HERE / "PAIRED_GROUP_DECOMPOSITION.csv", index=False)
    weights = []
    for label, frame in [("core", core), ("strict", strict)]:
        for field in ["corridor_group", "provider_group", "qidx"]:
            grouped = frame.groupby(field).agg(n=("stay", "size"), stays=("stay", "sum"), valid=("valid", "sum"), unknown=("unknown", "sum"))
            valid_groups = grouped[grouped.valid > 0]
            weights.append(dict(identity_rule=label, weighting="equal_"+field, total_groups=len(grouped),
                groups_with_valid_pairs=len(valid_groups), conditional=(valid_groups.stays/valid_groups.valid).mean(),
                lower=(grouped.stays/grouped.n).mean(), upper=((grouped.stays+grouped.unknown)/grouped.n).mean(),
                interpretation="DIFFERENT_DESCRIPTIVE_ESTIMAND_NOT_POPULATION_CORRECTION"))
    m.pd.DataFrame(weights).to_csv(HERE / "WEIGHTING_SUPPORT.csv", index=False)
    assumed = []
    for fraction in [0, .01, .05, .10]:
        row = adversarial_false_positive(45343, 29546, 6883, math.floor(36429*fraction))
        row.update(assumed_fraction_of_valid_links=fraction, status="ILLUSTRATIVE_ASSUMPTION_NOT_EMPIRICAL_ERROR_RATE")
        assumed.append(row)
    m.pd.DataFrame(assumed).to_csv(HERE / "ILLUSTRATIVE_LINKAGE_SENSITIVITY.csv", index=False)
    # Reconcile from an independent existing wave table, not the new grouped output.
    prior = m.pd.read_csv(ROOT / "research_completion/phase3/followup_20261021/attribute_change_by_wave.csv")
    assert prior.n_changed_valid.sum() == 5859
    assert sum(r["newly_unknown"] for r in paired if r["group_field"] == "source_era") == 5859
    assert sum(r["changed_core_stay"] for r in paired if r["group_field"] == "source_era") == 4770
    manifest = dict(phase3_raw_source_hash=m.EXPECTED, cached_records=len(records), primary_counts_unchanged=True,
                    n_origins=45343, core_valid=36429, strict_valid=30570, newly_unknown=5859,
                    new_classifier_fits=0, estimates_replaced_by_machine_labels=False,
                    scope="POST_FREEZE_FINITE_PANEL_DESCRIPTIONS_NO_CAUSAL_TEST")
    (HERE / "measurement_check.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
