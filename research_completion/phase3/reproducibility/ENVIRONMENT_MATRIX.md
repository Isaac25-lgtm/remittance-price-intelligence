# Environment matrix

| run | python | platform | numpy | pandas | scipy | sklearn |
| --- | --- | --- | --- | --- | --- | --- |
| locked_real_1 | 3.12.10 | Windows-11-10.0.26200-SP0 | 2.5.4 | 3.0.6 | 1.16.1 | 1.9.1 |
| base_real_1 | 3.12.10 | Windows-11-10.0.26200-SP0 | 2.2.5 | 2.2.3 | 1.16.1 | 1.6.1 |
| locked_fixture_1 | 3.12.10 | Windows-11-10.0.26200-SP0 | 2.5.4 | 3.0.6 | 1.16.1 | 1.9.1 |
| base_fixture_1 | 3.12.10 | Windows-11-10.0.26200-SP0 | 2.2.5 | 2.2.3 | 1.16.1 | 1.6.1 |
| tight_real_1 | 3.12.10 | Windows-11-10.0.26200-SP0 | 2.5.4 | 3.0.6 | 1.16.1 | 1.9.1 |

The legacy Linux report records Python 3.13.16, numpy 2.5.4, pandas 3.0.6 and sklearn 1.9.1. Thus a casual claim that all differences were caused by an sklearn upgrade would be false: the original scientific stack already matches those locked library versions. Windows uses Python 3.12.10 and recorded local BLAS DLLs; original Linux transformed rows/probabilities/BLAS fingerprints were not preserved. The base older Windows stack is a controlled alternate, not a reconstruction of original Linux.

All logged fits cap BLAS/OMP/MKL/NumExpr at two threads with PYTHONHASHSEED0. Full threadpool paths/versions and split/transformation/prediction hashes appear in each run JSON. Hashes are fingerprints only; no records or predictions are public. Within-environment repeats are exact, using absolute/relative tolerance zero. The original cross-platform 1e-9 comparator is unchanged and still fails. No post hoc substantive tolerance has been introduced. The small cross-dependency synthetic fixture happens to agree exactly; this does not prove real-data identity.

The original strict 1e-9 comparator still has 14 exact matches,2 timing-only matches and 14 differing tables. Independent count checks match in all 20 fields tested. Separate locked Windows runs give exactly equal ridge and spline predictions on the selected 2022 fold; this is not proof of Linux numeric identity. [R01]

On the inspected 2022 legacy fold, tightening the fixed diagnostic tolerance from 1e-4 to 1e-10 changes ridge Brier from 0.156476196 to 0.156857164, and spline from 0.154414433 to 0.154575503. Maximum individual probability changes are 0.081154 and 0.041055. These probes are not new selected candidates. [R02]

The older-stack real fold has identical input-row hashes but different transformed-array hashes and tiny Brier/probability differences. Tightening the solver changes individual probabilities substantially more than the original platform differences. This demonstrates preprocessing/termination sensitivity, not an identified causal explanation for the original Linux residual. Larger optimization precision is not uniformly better out of sample in the probe. Frozen scores remain scores of the declared algorithm/tolerance; mathematical optimum and stable individual decisions are not claimed. Reviving a predictive paper would require locked cross-platform row fingerprints and prespecified convergence/refit validation; it is not a reason to repeat the broad model search for TrackA.
