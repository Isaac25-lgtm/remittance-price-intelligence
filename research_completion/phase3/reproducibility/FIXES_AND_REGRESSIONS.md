# Repairs and regressions

A genuine invalid-cost boundary defect was fixed: infinite target costs now remain unknown. Across 408,938 source cost cells, there are 0 infinite costs, so this repair changes no observed source result. [R03]

New primary finite-cost guards affect `primary_outcome_rows` and the observed-failure count in `bounds_table`; regression cases cover NaN, negative and infinite target costs. The independent source parser already used finite validation. Historical source/results/config bytes are preserved; the source implementation change is intentional and listed in the final audit.

The first Phase 3 comparison command successfully generated its audit but returned exit 0 despite retained DIFFERS statuses. The wrapper now returns the original comparator's failing exit code; the corrected run records exit 1 as expected negative evidence. Report-writing success is not strict numeric reproduction success. No tolerance was widened. Every mismatched numeric field is recorded in LEGACY_FIELD_DIFFERENCES.csv; all 30 files are partitioned in LEGACY_DIFFERENCE_CAUSES.csv.

The private review aid was repaired to include alternate metadata candidates and a separate blinded stratum key. No identity rule, outcome or external adjudication was changed. Missing-wave mutation detection demonstrates that the adversarial oracle fails under a deliberately wrong bridge. Clock, nonfinite-cost, duplicate, speed-change, weighting and asymmetric-cluster fixtures protect scientific semantics. Successful synthetic tests are not observed human validation.

Final documentation repairs preserve literal SHA/ISO-date tokens during prose spacing and validate relative links after the audit report exists. Regression and literal-token audit checks cover these presentation/provenance defects; no scientific numerator, model score or source value changed.
