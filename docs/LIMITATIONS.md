# Limitations

1. **Quotes, not transactions.** RPW records surveyed offers for fixed USD 200/500 baskets. Nothing here measures prices paid, volumes, market shares, provider exit or consumer savings.
2. **Conditional target.** E1 is defined only for quotes reobserved at t+1. Non-reobservation is common, and in 2021 and 2025 it is extreme. The E2 bounds are wide in those years.
3. **No release dates.** Lead time for any "forecast" is unestablished. Results are retrospective measurement and triage benchmarks only.
4. **No untouched test data.** 2022–24 were inspected in the pilot. 2025 contributes only 2025Q1 targets (2025Q2 is absent), and those were also present in the pilot's workbook.
5. **Identity is label-based.** Provider and attribute strings change over time, for example around 2021 and at the 2022Q4 jump in row counts. Exact-key linkage is conservative and probably under-links renamed services. Missing does not mean exit.
6. **Dependence.** The bootstraps are one-way (corridor or provider), not crossed. Quotes from the same provider across corridors and the same quarter are correlated.
7. **Pilot discrepancy.** The pilot code and inputs were unavailable. The difference of 18 test rows and the different spline/history specifications cannot be fully explained.
8. **Subgroups.** Uganda (receiving: 3 corridors, 20 test failures; sending: none) does not support model claims. Sub-Saharan Africa differences are not statistically distinguishable.
9. **Single threshold-crossing outcome.** A quote moving from 2.99% to 3.01% counts as a failure; the 5% sensitivity is provided for this reason.
