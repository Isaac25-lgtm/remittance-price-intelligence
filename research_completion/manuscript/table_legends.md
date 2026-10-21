# Table legends and provenance

Tables are deterministic exports of independently checked measurement or executed model aggregates. Legacy versus phase2 is explicit in analysis fields. All intervals are exploratory and conditional on fitted predictions; see the dependence methods and simulation caveats.

- [supplementary_corridor_estimand](../tables/supplementary_corridor_estimand.md): 10 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [supplementary_cost_transitions](../tables/supplementary_cost_transitions.md): 8 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [supplementary_descriptive_groups](../tables/supplementary_descriptive_groups.md): 36 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [supplementary_fee_fx_changes](../tables/supplementary_fee_fx_changes.md): 2 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [supplementary_overall_bounds](../tables/supplementary_overall_bounds.md): 1 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [supplementary_threshold_margin](../tables/supplementary_threshold_margin.md): 6 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_01_source_flow](../tables/table_01_source_flow.md): 199 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_02_profile](../tables/table_02_profile.md): 37 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_03_persistence_bounds](../tables/table_03_persistence_bounds.md): 36 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_04_split_features](../tables/table_04_split_features.md): 24 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_05_models](../tables/table_05_models.md): 88 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_06_decision_capacity](../tables/table_06_decision_capacity.md): 80 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_07_transfer_subgroups](../tables/table_07_transfer_subgroups.md): 206 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.
- [table_08_sensitivities](../tables/table_08_sensitivities.md): 15 aggregate rows. See field names and canonical report; probabilities/percentage points/counts as labelled.

Table 1: exclusive initially-cheap origin flow by assigned calendar quarter, 2016Q2–2025Q3; counts include final-wave right censoring. Table 2: all post-2016 source quote records by wave; costs are percent of the USD200 transfer, dates are collection dates, shares are survey-record proportions. Table 3: exact-next-quarter E1 conditional stay and E2 all-origin bounds; corridor intervals are nominal95%, not missing-data bounds. Table 4: annual2022–2025Q1 outer target periods and strictly earlier training/tuning/calibration/selection windows, row/event/group counts.

Table 5 reports absolute Brier/log-loss with resampling labels; paired differences are in models/paired_dependence.csv and joint_dependence_sensitivity.csv. Table 6 is the future-reobserved E1 benchmark at5/10/20/30% per-quarter budget; the corrected all-origin queue and unknown-state recall bounds are in models/all_origin_capacity_bounds.csv. Table 7 applies the100-failure/cluster support gates; true group transfer is separately in transfer_sensitivity_metrics.csv. Table 8 reports distinct scenario denominators, not paired causal effects. The final fitted source/dominance stresses are in models/final_stress_metrics.csv.

S1–S6 are mapped in supplementary_material.md. No individual-provider assessments or restricted rows are included.
