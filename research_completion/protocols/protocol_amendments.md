# Protocol amendments

2026-10-20: Initial local completion specification committed before phase-2 metrics. Historical pilot and phase-1 scores had already been viewed. All new analyses remain retrospective/exploratory.

Append dated amendments before any affected new metric. Do not rewrite prior choices after performance is seen.

2026-10-20, before all phase-2 metrics: Split the inner temporal window into six target quarters: two for bounded hyperparameter tuning, two for fitting calibrators and two for selecting raw/sigmoid/isotonic methods. This replaces the initial four-quarter wording and prevents fitting and assessing calibration on the same records. Base models are refit using proper-training plus tuning records, then frozen through calibration/selection and outer scoring. All phase-2 families share that training cut. The legacy full-training benchmark remains separate. Selection estimates are exploratory, not unbiased test estimates. No phase-2 scores had been calculated at amendment time.

2026-10-20, before phase-2 metrics: The downloaded official Issue 54 report documents Russia collection-method changes after 2022Q2 and prospects-index changes in 2025Q3. Add an exclude-Russia sensitivity and separate pre/post-2022 composition summaries. The PDF's September 2025 publication statement and April 2026 creation metadata conflict; neither alone establishes first public availability.
