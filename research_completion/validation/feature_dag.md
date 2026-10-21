# Feature information graph

```mermaid
flowchart LR
  A[Origin surveyed quotes and collection dates] --> B[Current cost / fee / FX / channel]
  A --> C[Origin corridor composition]
  D[Earlier exact-quarter linked outcomes] --> E[Past-only smoothed histories]
  F[Earlier own unique quote] --> G[Prior cost and change]
  B --> H[Fold-trained imputer / encoder / scaler / spline]
  C --> H
  E --> H
  G --> H
  H --> I[Earlier trained probability model]
  I --> J[Separate chronological calibrator / selector]
  J --> K[Retrospective outer predictions]
  L[Future target quotes and observation status] --> M[E1 cohort / labels / E2 unknown states]
  K --> N[Evaluation conditional on E1 or all-origin bounds]
  M --> N
  O[Historical public release clocks UNVERIFIED] --> P[Operational early-warning claim rejected]
```

No arrow from future outcomes/status into admissible features. Whole-origin-wave composition is only retrospectively available here. All heldout-group target outcomes are removed from historical event pools. E1 membership itself depends on future reobservation and is explicitly an evaluation selection; the corrected all-origin review scenario preserves unknown states. Public release timing remains a separate failed forecasting gate. See feature_asof_registry.csv and the executable leakage/future-clock tests.
