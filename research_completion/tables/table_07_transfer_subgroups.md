# table 07 transfer subgroups

| analysis | group | model | n | failures | n_corridors | supported | prevalence_stay | brier | log_loss | cal_intercept | cal_slope | mean_pred | auroc | auprc_failure | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy | SSA | B0_always_stay | 2779 | 688 | 74 | True | 0.752429 | 0.247571 | 3.42032 | -12.7039 |  | 0.999999 | 0.5 | 0.247571 |  |
| legacy | SSA | B1_prevalence | 2779 | 688 | 74 | True | 0.752429 | 0.188977 | 0.567719 | -0.301923 | 0.524048 | 0.804322 | 0.506779 | 0.248493 |  |
| legacy | SSA | B2_history | 2779 | 688 | 74 | True | 0.752429 | 0.179351 | 0.548047 | -0.304279 | 0.607839 | 0.798671 | 0.661006 | 0.366039 |  |
| legacy | SSA | B3_cost_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.183743 | 0.565216 | -0.21036 | 0.453453 | 0.787584 | 0.608529 | 0.326865 |  |
| legacy | SSA | L1_ridge_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.168263 | 0.515564 | -0.134905 | 0.719579 | 0.772466 | 0.717115 | 0.438324 |  |
| legacy | SSA | L2_spline_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.167707 | 0.516847 | -0.190589 | 0.697833 | 0.780098 | 0.712397 | 0.449697 |  |
| legacy | SSA | M1_hist_gbm | 2779 | 688 | 74 | True | 0.752429 | 0.162431 | 0.5007 | 0.101586 | 0.737294 | 0.737363 | 0.731788 | 0.485084 |  |
| legacy | SSA | M2_random_forest | 2779 | 688 | 74 | True | 0.752429 | 0.160585 | 0.493952 | -0.0473291 | 1.06098 | 0.760118 | 0.733608 | 0.487509 |  |
| legacy | EAC | B0_always_stay | 731 | 137 | 25 | True | 0.812585 | 0.187414 | 2.58923 | -12.3486 |  | 0.999999 | 0.5 | 0.187415 |  |
| legacy | EAC | B1_prevalence | 731 | 137 | 25 | True | 0.812585 | 0.152304 | 0.482497 | 0.0536674 | 0.692548 | 0.804275 | 0.562111 | 0.209328 |  |
| legacy | EAC | B2_history | 731 | 137 | 25 | True | 0.812585 | 0.136559 | 0.441788 | -0.0742897 | 0.888927 | 0.822471 | 0.699286 | 0.395967 |  |
| legacy | EAC | B3_cost_logistic | 731 | 137 | 25 | True | 0.812585 | 0.153412 | 0.490466 | 0.213183 | 0.365982 | 0.779236 | 0.58321 | 0.25923 |  |
| legacy | EAC | L1_ridge_logistic | 731 | 137 | 25 | True | 0.812585 | 0.119648 | 0.391409 | 0.180633 | 1.01622 | 0.78996 | 0.795473 | 0.507833 |  |
| legacy | EAC | L2_spline_logistic | 731 | 137 | 25 | True | 0.812585 | 0.123889 | 0.40238 | 0.229901 | 0.903407 | 0.783958 | 0.778183 | 0.493754 |  |
| legacy | EAC | M1_hist_gbm | 731 | 137 | 25 | True | 0.812585 | 0.123453 | 0.404161 | 0.468862 | 0.927965 | 0.752004 | 0.792438 | 0.526795 |  |
| legacy | EAC | M2_random_forest | 731 | 137 | 25 | True | 0.812585 | 0.124585 | 0.406762 | 0.27866 | 1.24835 | 0.772866 | 0.774448 | 0.505951 |  |
| legacy | Uganda | B0_always_stay | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | B1_prevalence | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | B2_history | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | B3_cost_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | L1_ridge_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | L2_spline_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | M1_hist_gbm | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| legacy | Uganda | M2_random_forest | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | SSA | B0_always_stay | 2779 | 688 | 74 | True | 0.752429 | 0.247571 | 3.42032 | -12.7039 |  | 0.999999 | 0.5 | 0.247571 |  |
| phase2 | SSA | B1_prevalence | 2779 | 688 | 74 | True | 0.752429 | 0.188818 | 0.567218 | -0.288073 | -3.8562 | 0.802131 | 0.475757 | 0.238606 |  |
| phase2 | SSA | B2_history | 2779 | 688 | 74 | True | 0.752429 | 0.179351 | 0.548047 | -0.304279 | 0.607839 | 0.798671 | 0.661006 | 0.366039 |  |
| phase2 | SSA | B3_cost_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.183606 | 0.566011 | -0.178382 | 0.430476 | 0.782312 | 0.608668 | 0.326559 |  |
| phase2 | SSA | L1_ridge_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.177737 | 0.553444 | -0.311012 | 0.511399 | 0.795044 | 0.694708 | 0.421155 |  |
| phase2 | SSA | L1_ridge_logistic__cal | 2779 | 688 | 74 | True | 0.752429 | 0.1734 | 0.529642 | -0.277754 | 0.734284 | 0.794241 | 0.693382 | 0.411616 |  |
| phase2 | SSA | L2_spline_logistic | 2779 | 688 | 74 | True | 0.752429 | 0.176508 | 0.554276 | -0.418528 | 0.532062 | 0.808224 | 0.686794 | 0.428618 |  |
| phase2 | SSA | L2_spline_logistic__cal | 2779 | 688 | 74 | True | 0.752429 | 0.173518 | 0.543326 | -0.347569 | 0.611439 | 0.802764 | 0.683539 | 0.425979 |  |
| phase2 | SSA | M1_hist_gbm | 2779 | 688 | 74 | True | 0.752429 | 0.159155 | 0.491639 | -0.114909 | 0.879942 | 0.769707 | 0.737966 | 0.499338 |  |
| phase2 | SSA | M1_hist_gbm__cal | 2779 | 688 | 74 | True | 0.752429 | 0.159036 | 0.491629 | -0.100882 | 0.917756 | 0.767882 | 0.737585 | 0.500932 |  |
| phase2 | SSA | M2_random_forest | 2779 | 688 | 74 | True | 0.752429 | 0.161871 | 0.495771 | -0.091531 | 1.12245 | 0.767358 | 0.732374 | 0.476029 |  |
| phase2 | SSA | M2_random_forest__cal | 2779 | 688 | 74 | True | 0.752429 | 0.161956 | 0.499297 | -0.125781 | 0.940947 | 0.772167 | 0.728917 | 0.477019 |  |
| phase2 | SSA | S_selected | 2779 | 688 | 74 | True | 0.752429 | 0.164141 | 0.505932 | -0.0906321 | 0.828851 | 0.766378 | 0.720105 | 0.456688 |  |
| phase2 | SSA | B4_recent_history | 2779 | 688 | 74 | True | 0.752429 | 0.180347 | 0.550956 | -0.337643 | 0.638636 | 0.804497 | 0.646764 | 0.365976 |  |
| phase2 | EAC | B0_always_stay | 731 | 137 | 25 | True | 0.812585 | 0.187414 | 2.58923 | -12.3486 |  | 0.999999 | 0.5 | 0.187415 |  |
| phase2 | EAC | B1_prevalence | 731 | 137 | 25 | True | 0.812585 | 0.152435 | 0.482913 | 0.0664055 | 0.693267 | 0.802263 | 0.452377 | 0.180123 |  |
| phase2 | EAC | B2_history | 731 | 137 | 25 | True | 0.812585 | 0.136559 | 0.441788 | -0.0742897 | 0.888927 | 0.822471 | 0.699286 | 0.395967 |  |
| phase2 | EAC | B3_cost_logistic | 731 | 137 | 25 | True | 0.812585 | 0.154258 | 0.493454 | 0.247737 | 0.33752 | 0.773627 | 0.58353 | 0.259605 |  |
| phase2 | EAC | L1_ridge_logistic | 731 | 137 | 25 | True | 0.812585 | 0.120823 | 0.394085 | -0.0573066 | 0.932588 | 0.819204 | 0.790496 | 0.492865 |  |
| phase2 | EAC | L1_ridge_logistic__cal | 731 | 137 | 25 | True | 0.812585 | 0.1236 | 0.401466 | -0.00923732 | 1.05953 | 0.813745 | 0.782564 | 0.482626 |  |
| phase2 | EAC | L2_spline_logistic | 731 | 137 | 25 | True | 0.812585 | 0.126235 | 0.408892 | -0.0322661 | 0.789215 | 0.816226 | 0.771449 | 0.472208 |  |
| phase2 | EAC | L2_spline_logistic__cal | 731 | 137 | 25 | True | 0.812585 | 0.125982 | 0.411582 | 0.0257799 | 0.853516 | 0.809452 | 0.763536 | 0.483281 |  |
| phase2 | EAC | M1_hist_gbm | 731 | 137 | 25 | True | 0.812585 | 0.120652 | 0.394547 | 0.248987 | 1.02244 | 0.780408 | 0.785175 | 0.526862 |  |
| phase2 | EAC | M1_hist_gbm__cal | 731 | 137 | 25 | True | 0.812585 | 0.121765 | 0.39937 | 0.251301 | 1.03706 | 0.779499 | 0.77881 | 0.523166 |  |
| phase2 | EAC | M2_random_forest | 731 | 137 | 25 | True | 0.812585 | 0.124753 | 0.406483 | 0.256694 | 1.3265 | 0.775667 | 0.77822 | 0.509062 |  |
| phase2 | EAC | M2_random_forest__cal | 731 | 137 | 25 | True | 0.812585 | 0.123716 | 0.405382 | 0.233958 | 1.11096 | 0.780528 | 0.77226 | 0.523928 |  |
| phase2 | EAC | S_selected | 731 | 137 | 25 | True | 0.812585 | 0.121706 | 0.401653 | 0.250649 | 1.02854 | 0.779551 | 0.779056 | 0.494491 |  |
| phase2 | EAC | B4_recent_history | 731 | 137 | 25 | True | 0.812585 | 0.138767 | 0.447542 | -0.120101 | 0.901193 | 0.828592 | 0.681056 | 0.382448 |  |
| phase2 | Uganda | B0_always_stay | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | B1_prevalence | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | B2_history | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | B3_cost_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | L1_ridge_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | L1_ridge_logistic__cal | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | L2_spline_logistic | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | L2_spline_logistic__cal | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | M1_hist_gbm | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | M1_hist_gbm__cal | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | M2_random_forest | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | M2_random_forest__cal | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | S_selected | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | Uganda | B4_recent_history | 140 | 20 | 3 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Upper middle income | B0_always_stay | 3924 | 827 | 113 | True | 0.789246 | 0.210754 | 2.91168 | -12.4951 |  | 0.999999 | 0.5 | 0.210754 |  |
| phase2 | income: Upper middle income | B1_prevalence | 3924 | 827 | 113 | True | 0.789246 | 0.16643 | 0.515241 | -0.0772481 | 0.625802 | 0.801807 | 0.507038 | 0.217591 |  |
| phase2 | income: Upper middle income | B2_history | 3924 | 827 | 113 | True | 0.789246 | 0.155237 | 0.489434 | -0.264328 | 0.681959 | 0.824815 | 0.68781 | 0.366753 |  |
| phase2 | income: Upper middle income | B3_cost_logistic | 3924 | 827 | 113 | True | 0.789246 | 0.162694 | 0.511196 | 0.0918811 | 0.541285 | 0.774464 | 0.624312 | 0.289876 |  |
| phase2 | income: Upper middle income | L1_ridge_logistic | 3924 | 827 | 113 | True | 0.789246 | 0.151957 | 0.479713 | -0.371597 | 0.77087 | 0.837087 | 0.709456 | 0.4067 |  |
| phase2 | income: Upper middle income | L1_ridge_logistic__cal | 3924 | 827 | 113 | True | 0.789246 | 0.151909 | 0.477418 | -0.294218 | 0.871397 | 0.829375 | 0.701188 | 0.400862 |  |
| phase2 | income: Upper middle income | L2_spline_logistic | 3924 | 827 | 113 | True | 0.789246 | 0.151361 | 0.477914 | -0.456344 | 0.767557 | 0.845802 | 0.723684 | 0.417957 |  |
| phase2 | income: Upper middle income | L2_spline_logistic__cal | 3924 | 827 | 113 | True | 0.789246 | 0.150715 | 0.47627 | -0.361375 | 0.822082 | 0.836816 | 0.719207 | 0.408847 |  |
| phase2 | income: Upper middle income | M1_hist_gbm | 3924 | 827 | 113 | True | 0.789246 | 0.143521 | 0.449509 | -0.223127 | 0.915379 | 0.818754 | 0.751622 | 0.452627 |  |
| phase2 | income: Upper middle income | M1_hist_gbm__cal | 3924 | 827 | 113 | True | 0.789246 | 0.144486 | 0.45476 | -0.218797 | 0.902598 | 0.818531 | 0.742649 | 0.447869 |  |
| phase2 | income: Upper middle income | M2_random_forest | 3924 | 827 | 113 | True | 0.789246 | 0.14311 | 0.446306 | -0.0477851 | 1.09459 | 0.796167 | 0.752678 | 0.449951 |  |
| phase2 | income: Upper middle income | M2_random_forest__cal | 3924 | 827 | 113 | True | 0.789246 | 0.144126 | 0.453042 | -0.107455 | 0.879128 | 0.804025 | 0.744304 | 0.443675 |  |
| phase2 | income: Upper middle income | S_selected | 3924 | 827 | 113 | True | 0.789246 | 0.14689 | 0.461234 | -0.197697 | 0.897306 | 0.816231 | 0.729111 | 0.430704 |  |
| phase2 | income: Upper middle income | B4_recent_history | 3924 | 827 | 113 | True | 0.789246 | 0.157931 | 0.496003 | -0.304787 | 0.69828 | 0.830843 | 0.671038 | 0.350071 |  |
| phase2 | income: Lower middle income | B0_always_stay | 13414 | 2446 | 195 | True | 0.817653 | 0.182346 | 2.51921 | -12.315 |  | 0.999999 | 0.5 | 0.182347 |  |
| phase2 | income: Lower middle income | B1_prevalence | 13414 | 2446 | 195 | True | 0.817653 | 0.149301 | 0.475591 | 0.102479 | 0.710696 | 0.801875 | 0.517728 | 0.188814 |  |
| phase2 | income: Lower middle income | B2_history | 13414 | 2446 | 195 | True | 0.817653 | 0.139178 | 0.443309 | 0.00489168 | 0.801075 | 0.816995 | 0.686495 | 0.329886 |  |
| phase2 | income: Lower middle income | B3_cost_logistic | 13414 | 2446 | 195 | True | 0.817653 | 0.144818 | 0.462865 | 0.191049 | 0.738769 | 0.789148 | 0.646921 | 0.277155 |  |
| phase2 | income: Lower middle income | L1_ridge_logistic | 13414 | 2446 | 195 | True | 0.817653 | 0.135283 | 0.440053 | -0.263461 | 0.666534 | 0.847427 | 0.730486 | 0.376181 |  |
| phase2 | income: Lower middle income | L1_ridge_logistic__cal | 13414 | 2446 | 195 | True | 0.817653 | 0.133654 | 0.430776 | -0.174803 | 0.825132 | 0.839082 | 0.729994 | 0.375475 |  |
| phase2 | income: Lower middle income | L2_spline_logistic | 13414 | 2446 | 195 | True | 0.817653 | 0.135759 | 0.440981 | -0.279395 | 0.647226 | 0.848715 | 0.729494 | 0.37386 |  |
| phase2 | income: Lower middle income | L2_spline_logistic__cal | 13414 | 2446 | 195 | True | 0.817653 | 0.134319 | 0.439898 | -0.191485 | 0.682978 | 0.840619 | 0.727013 | 0.371367 |  |
| phase2 | income: Lower middle income | M1_hist_gbm | 13414 | 2446 | 195 | True | 0.817653 | 0.127829 | 0.407973 | -0.0194722 | 0.945697 | 0.820086 | 0.761609 | 0.422637 |  |
| phase2 | income: Lower middle income | M1_hist_gbm__cal | 13414 | 2446 | 195 | True | 0.817653 | 0.127798 | 0.408914 | -0.0129592 | 0.977582 | 0.819297 | 0.760056 | 0.423372 |  |
| phase2 | income: Lower middle income | M2_random_forest | 13414 | 2446 | 195 | True | 0.817653 | 0.127369 | 0.40701 | 0.14361 | 1.25402 | 0.797728 | 0.770249 | 0.425986 |  |
| phase2 | income: Lower middle income | M2_random_forest__cal | 13414 | 2446 | 195 | True | 0.817653 | 0.127251 | 0.407136 | 0.0824676 | 1.04348 | 0.806772 | 0.765249 | 0.422058 |  |
| phase2 | income: Lower middle income | S_selected | 13414 | 2446 | 195 | True | 0.817653 | 0.130411 | 0.419073 | -0.0433203 | 0.892958 | 0.823115 | 0.750024 | 0.399175 |  |
| phase2 | income: Lower middle income | B4_recent_history | 13414 | 2446 | 195 | True | 0.817653 | 0.138092 | 0.4403 | -0.0871013 | 0.897662 | 0.829203 | 0.69075 | 0.33658 |  |
| phase2 | income: Low income | B0_always_stay | 835 | 171 | 42 | True | 0.79521 | 0.20479 | 2.82928 | -12.4589 |  | 0.999999 | 0.5 | 0.20479 |  |
| phase2 | income: Low income | B1_prevalence | 835 | 171 | 42 | True | 0.79521 | 0.162711 | 0.506532 | -0.0418757 | 12.9176 | 0.801945 | 0.560545 | 0.23225 |  |
| phase2 | income: Low income | B2_history | 835 | 171 | 42 | True | 0.79521 | 0.150816 | 0.472973 | -0.132154 | 0.727077 | 0.81335 | 0.696298 | 0.368598 |  |
| phase2 | income: Low income | B3_cost_logistic | 835 | 171 | 42 | True | 0.79521 | 0.164572 | 0.518361 | 0.234863 | 0.354402 | 0.756432 | 0.589243 | 0.242058 |  |
| phase2 | income: Low income | L1_ridge_logistic | 835 | 171 | 42 | True | 0.79521 | 0.150643 | 0.474939 | 0.271975 | 0.629206 | 0.757606 | 0.703216 | 0.430985 |  |
| phase2 | income: Low income | L1_ridge_logistic__cal | 835 | 171 | 42 | True | 0.79521 | 0.15127 | 0.475637 | 0.255389 | 0.757478 | 0.756885 | 0.701856 | 0.391302 |  |
| phase2 | income: Low income | L2_spline_logistic | 835 | 171 | 42 | True | 0.79521 | 0.148982 | 0.468675 | 0.163377 | 0.641375 | 0.773556 | 0.709954 | 0.429427 |  |
| phase2 | income: Low income | L2_spline_logistic__cal | 835 | 171 | 42 | True | 0.79521 | 0.147911 | 0.466597 | 0.193385 | 0.747746 | 0.767447 | 0.708355 | 0.408753 |  |
| phase2 | income: Low income | M1_hist_gbm | 835 | 171 | 42 | True | 0.79521 | 0.14441 | 0.444027 | 0.398746 | 0.888814 | 0.73828 | 0.768033 | 0.447786 |  |
| phase2 | income: Low income | M1_hist_gbm__cal | 835 | 171 | 42 | True | 0.79521 | 0.144203 | 0.446333 | 0.394654 | 0.923056 | 0.737536 | 0.764466 | 0.44468 |  |
| phase2 | income: Low income | M2_random_forest | 835 | 171 | 42 | True | 0.79521 | 0.144212 | 0.45032 | 0.342157 | 1.12865 | 0.741723 | 0.751185 | 0.427363 |  |
| phase2 | income: Low income | M2_random_forest__cal | 835 | 171 | 42 | True | 0.79521 | 0.145466 | 0.45416 | 0.333397 | 0.952936 | 0.74478 | 0.744685 | 0.427303 |  |
| phase2 | income: Low income | S_selected | 835 | 171 | 42 | True | 0.79521 | 0.147631 | 0.459354 | 0.399581 | 0.845983 | 0.736428 | 0.747296 | 0.40818 |  |
| phase2 | income: Low income | B4_recent_history | 835 | 171 | 42 | True | 0.79521 | 0.151087 | 0.475503 | -0.169 | 0.782712 | 0.818708 | 0.685377 | 0.37181 |  |
| phase2 | income: High income | B0_always_stay | 1305 | 110 | 16 | True | 0.915709 | 0.084291 | 1.16453 | -11.4301 |  | 0.999999 | 0.5 | 0.0842912 |  |
| phase2 | income: High income | B1_prevalence | 1305 | 110 | 16 | True | 0.915709 | 0.0898477 | 0.337707 | 0.981542 | 16.2814 | 0.802802 | 0.563906 | 0.101246 |  |
| phase2 | income: High income | B2_history | 1305 | 110 | 16 | True | 0.915709 | 0.0715478 | 0.256124 | 0.0342612 | 1.10223 | 0.913203 | 0.752769 | 0.218732 |  |
| phase2 | income: High income | B3_cost_logistic | 1305 | 110 | 16 | True | 0.915709 | 0.0891331 | 0.326529 | 0.866485 | 0.417981 | 0.827432 | 0.60065 | 0.139577 |  |
| phase2 | income: High income | L1_ridge_logistic | 1305 | 110 | 16 | True | 0.915709 | 0.0767572 | 0.279188 | 0.142511 | 0.602075 | 0.905465 | 0.700738 | 0.175169 |  |
| phase2 | income: High income | L1_ridge_logistic__cal | 1305 | 110 | 16 | True | 0.915709 | 0.0743787 | 0.27264 | 0.304766 | 0.871785 | 0.891036 | 0.71264 | 0.21911 |  |
| phase2 | income: High income | L2_spline_logistic | 1305 | 110 | 16 | True | 0.915709 | 0.0765646 | 0.273577 | 0.326163 | 0.677192 | 0.891068 | 0.724914 | 0.190972 |  |
| phase2 | income: High income | L2_spline_logistic__cal | 1305 | 110 | 16 | True | 0.915709 | 0.0758086 | 0.281875 | 0.444063 | 0.66732 | 0.878912 | 0.717661 | 0.19958 |  |
| phase2 | income: High income | M1_hist_gbm | 1305 | 110 | 16 | True | 0.915709 | 0.0668708 | 0.245473 | 0.28885 | 1.20657 | 0.893301 | 0.785135 | 0.341574 |  |
| phase2 | income: High income | M1_hist_gbm__cal | 1305 | 110 | 16 | True | 0.915709 | 0.0679265 | 0.250871 | 0.354006 | 1.20278 | 0.887281 | 0.778212 | 0.328649 |  |
| phase2 | income: High income | M2_random_forest | 1305 | 110 | 16 | True | 0.915709 | 0.0709367 | 0.263765 | 0.4964 | 1.30452 | 0.872157 | 0.763054 | 0.305897 |  |
| phase2 | income: High income | M2_random_forest__cal | 1305 | 110 | 16 | True | 0.915709 | 0.0704949 | 0.263161 | 0.401737 | 1.04576 | 0.882361 | 0.754481 | 0.298686 |  |
| phase2 | income: High income | S_selected | 1305 | 110 | 16 | True | 0.915709 | 0.0681937 | 0.252923 | 0.290795 | 1.23348 | 0.892501 | 0.767463 | 0.339484 |  |
| phase2 | income: High income | B4_recent_history | 1305 | 110 | 16 | True | 0.915709 | 0.0730177 | 0.261834 | -0.0808008 | 1.13401 | 0.92144 | 0.739418 | 0.201416 |  |
| phase2 | income: Lower income | B0_always_stay | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | B1_prevalence | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | B2_history | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | B3_cost_logistic | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | L1_ridge_logistic | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | L1_ridge_logistic__cal | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | L2_spline_logistic | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | L2_spline_logistic__cal | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | M1_hist_gbm | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | M1_hist_gbm__cal | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | M2_random_forest | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | M2_random_forest__cal | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | S_selected | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | income: Lower income | B4_recent_history | 189 | 51 | 27 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | B0_always_stay | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | B1_prevalence | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | B2_history | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | B3_cost_logistic | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | L1_ridge_logistic | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | L1_ridge_logistic__cal | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | L2_spline_logistic | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | L2_spline_logistic__cal | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | M1_hist_gbm | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | M1_hist_gbm__cal | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | M2_random_forest | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | M2_random_forest__cal | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | S_selected | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_provider_history | B4_recent_history | 93 | 38 | 64 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | provider_history_available | B0_always_stay | 19574 | 3567 | 328 | True | 0.817768 | 0.182231 | 2.51762 | -12.3142 |  | 0.999999 | 0.5 | 0.182232 |  |
| phase2 | provider_history_available | B1_prevalence | 19574 | 3567 | 328 | True | 0.817768 | 0.149213 | 0.475373 | 0.102748 | 4.41761 | 0.801955 | 0.518437 | 0.190066 |  |
| phase2 | provider_history_available | B2_history | 19574 | 3567 | 328 | True | 0.817768 | 0.138256 | 0.441269 | -0.0588994 | 0.780805 | 0.825455 | 0.694555 | 0.336153 |  |
| phase2 | provider_history_available | B3_cost_logistic | 19574 | 3567 | 328 | True | 0.817768 | 0.145491 | 0.465572 | 0.204377 | 0.68459 | 0.787221 | 0.642071 | 0.268381 |  |
| phase2 | provider_history_available | L1_ridge_logistic | 19574 | 3567 | 328 | True | 0.817768 | 0.135381 | 0.438871 | -0.243663 | 0.682604 | 0.845726 | 0.725735 | 0.37396 |  |
| phase2 | provider_history_available | L1_ridge_logistic__cal | 19574 | 3567 | 328 | True | 0.817768 | 0.134181 | 0.431859 | -0.157797 | 0.831898 | 0.837328 | 0.723632 | 0.371543 |  |
| phase2 | provider_history_available | L2_spline_logistic | 19574 | 3567 | 328 | True | 0.817768 | 0.135592 | 0.438822 | -0.271289 | 0.672184 | 0.848334 | 0.727524 | 0.373505 |  |
| phase2 | provider_history_available | L2_spline_logistic__cal | 19574 | 3567 | 328 | True | 0.817768 | 0.134388 | 0.438378 | -0.181873 | 0.711793 | 0.839802 | 0.724307 | 0.369533 |  |
| phase2 | provider_history_available | M1_hist_gbm | 19574 | 3567 | 328 | True | 0.817768 | 0.12766 | 0.407431 | -0.0314039 | 0.938639 | 0.821662 | 0.762865 | 0.422332 |  |
| phase2 | provider_history_available | M1_hist_gbm__cal | 19574 | 3567 | 328 | True | 0.817768 | 0.12788 | 0.40955 | -0.0222607 | 0.959097 | 0.820573 | 0.758934 | 0.421321 |  |
| phase2 | provider_history_available | M2_random_forest | 19574 | 3567 | 328 | True | 0.817768 | 0.127546 | 0.407556 | 0.125504 | 1.20807 | 0.800518 | 0.767522 | 0.422818 |  |
| phase2 | provider_history_available | M2_random_forest__cal | 19574 | 3567 | 328 | True | 0.817768 | 0.127672 | 0.409181 | 0.0663374 | 0.997898 | 0.809098 | 0.761418 | 0.419056 |  |
| phase2 | provider_history_available | S_selected | 19574 | 3567 | 328 | True | 0.817768 | 0.130238 | 0.41832 | -0.0416325 | 0.898851 | 0.823014 | 0.748708 | 0.400393 |  |
| phase2 | provider_history_available | B4_recent_history | 19574 | 3567 | 328 | True | 0.817768 | 0.138159 | 0.440825 | -0.139923 | 0.856126 | 0.835879 | 0.692894 | 0.336525 |  |
| phase2 | no_corridor_history | B0_always_stay | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | B1_prevalence | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | B2_history | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | B3_cost_logistic | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | L1_ridge_logistic | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | L1_ridge_logistic__cal | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | L2_spline_logistic | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | L2_spline_logistic__cal | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | M1_hist_gbm | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | M1_hist_gbm__cal | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | M2_random_forest | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | M2_random_forest__cal | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | S_selected | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | no_corridor_history | B4_recent_history | 22 | 7 | 9 | False |  |  |  |  |  |  |  |  | NOT_ESTIMABLE_SUPPORT_GATE |
| phase2 | remote_initiation | B0_always_stay | 13939 | 2263 | 299 | True | 0.83765 | 0.16235 | 2.24295 | -12.1747 |  | 0.999999 | 0.5 | 0.16235 |  |
| phase2 | remote_initiation | B1_prevalence | 13939 | 2263 | 299 | True | 0.83765 | 0.137235 | 0.447656 | 0.241851 | 0.776649 | 0.802026 | 0.508508 | 0.165954 |  |
| phase2 | remote_initiation | B2_history | 13939 | 2263 | 299 | True | 0.83765 | 0.128071 | 0.417155 | 0.0180592 | 0.744784 | 0.83543 | 0.684452 | 0.294876 |  |
| phase2 | remote_initiation | B3_cost_logistic | 13939 | 2263 | 299 | True | 0.83765 | 0.134235 | 0.438715 | 0.306347 | 0.683127 | 0.794332 | 0.644387 | 0.247109 |  |
| phase2 | remote_initiation | L1_ridge_logistic | 13939 | 2263 | 299 | True | 0.83765 | 0.124745 | 0.411406 | -0.315615 | 0.72321 | 0.870923 | 0.722967 | 0.347276 |  |
| phase2 | remote_initiation | L1_ridge_logistic__cal | 13939 | 2263 | 299 | True | 0.83765 | 0.123565 | 0.403681 | -0.190449 | 0.910859 | 0.859511 | 0.719727 | 0.34337 |  |
| phase2 | remote_initiation | L2_spline_logistic | 13939 | 2263 | 299 | True | 0.83765 | 0.124538 | 0.410354 | -0.374129 | 0.719653 | 0.875957 | 0.728917 | 0.348401 |  |
| phase2 | remote_initiation | L2_spline_logistic__cal | 13939 | 2263 | 299 | True | 0.83765 | 0.123527 | 0.412073 | -0.241328 | 0.734959 | 0.864408 | 0.723682 | 0.341989 |  |
| phase2 | remote_initiation | M1_hist_gbm | 13939 | 2263 | 299 | True | 0.83765 | 0.11646 | 0.379322 | -0.0692491 | 1.02253 | 0.845635 | 0.765403 | 0.405507 |  |
| phase2 | remote_initiation | M1_hist_gbm__cal | 13939 | 2263 | 299 | True | 0.83765 | 0.116875 | 0.381763 | -0.0465686 | 1.04102 | 0.843115 | 0.760961 | 0.403341 |  |
| phase2 | remote_initiation | M2_random_forest | 13939 | 2263 | 299 | True | 0.83765 | 0.117144 | 0.381164 | 0.119476 | 1.26972 | 0.822414 | 0.769405 | 0.403602 |  |
| phase2 | remote_initiation | M2_random_forest__cal | 13939 | 2263 | 299 | True | 0.83765 | 0.117169 | 0.382399 | 0.0436182 | 1.04449 | 0.832367 | 0.762098 | 0.39853 |  |
| phase2 | remote_initiation | S_selected | 13939 | 2263 | 299 | True | 0.83765 | 0.119711 | 0.39029 | -0.0623081 | 0.971938 | 0.844959 | 0.747593 | 0.375067 |  |
| phase2 | remote_initiation | B4_recent_history | 13939 | 2263 | 299 | True | 0.83765 | 0.12754 | 0.415187 | -0.0300452 | 0.822461 | 0.84134 | 0.682386 | 0.298815 |  |
| phase2 | other_initiation | B0_always_stay | 5728 | 1342 | 251 | True | 0.765712 | 0.234287 | 3.23681 | -12.6313 |  | 0.999999 |  |  |  |
| phase2 | other_initiation | B1_prevalence | 5728 | 1342 | 251 | True | 0.765712 | 0.180562 | 0.547907 | -0.2131 | 6.96466 | 0.801762 | 0.537294 | 0.251813 |  |
| phase2 | other_initiation | B2_history | 5728 | 1342 | 251 | True | 0.765712 | 0.165483 | 0.506207 | -0.228719 | 0.781908 | 0.799754 | 0.693529 | 0.404254 |  |
| phase2 | other_initiation | B3_cost_logistic | 5728 | 1342 | 251 | True | 0.765712 | 0.174962 | 0.536517 | -0.021713 | 0.590484 | 0.769374 | 0.620621 | 0.313326 |  |
| phase2 | other_initiation | L1_ridge_logistic | 5728 | 1342 | 251 | True | 0.765712 | 0.163281 | 0.51056 | -0.10615 | 0.615195 | 0.780597 | 0.713581 | 0.423156 |  |
| phase2 | other_initiation | L1_ridge_logistic__cal | 5728 | 1342 | 251 | True | 0.765712 | 0.16182 | 0.504521 | -0.0983525 | 0.712983 | 0.780304 | 0.713363 | 0.420928 |  |
| phase2 | other_initiation | L2_spline_logistic | 5728 | 1342 | 251 | True | 0.765712 | 0.164413 | 0.512855 | -0.0753588 | 0.599126 | 0.776333 | 0.708047 | 0.42075 |  |
| phase2 | other_initiation | L2_spline_logistic__cal | 5728 | 1342 | 251 | True | 0.765712 | 0.162617 | 0.506372 | -0.0685955 | 0.668786 | 0.77591 | 0.707691 | 0.419642 |  |
| phase2 | other_initiation | M1_hist_gbm | 5728 | 1342 | 251 | True | 0.765712 | 0.156446 | 0.479405 | 0.0383716 | 0.826564 | 0.760058 | 0.741348 | 0.465548 |  |
| phase2 | other_initiation | M1_hist_gbm__cal | 5728 | 1342 | 251 | True | 0.765712 | 0.156235 | 0.480834 | 0.0201621 | 0.842926 | 0.76271 | 0.738576 | 0.465389 |  |
| phase2 | other_initiation | M2_random_forest | 5728 | 1342 | 251 | True | 0.765712 | 0.154621 | 0.475927 | 0.129517 | 1.13453 | 0.744579 | 0.747639 | 0.463077 |  |
| phase2 | other_initiation | M2_random_forest__cal | 5728 | 1342 | 251 | True | 0.765712 | 0.155127 | 0.478799 | 0.103138 | 0.932008 | 0.749628 | 0.743593 | 0.459183 |  |
| phase2 | other_initiation | S_selected | 5728 | 1342 | 251 | True | 0.765712 | 0.157658 | 0.490673 | -0.00607773 | 0.781455 | 0.766617 | 0.735194 | 0.446493 |  |
| phase2 | other_initiation | B4_recent_history | 5728 | 1342 | 251 | True | 0.765712 | 0.166442 | 0.509479 | -0.381008 | 0.859231 | 0.820995 | 0.699134 | 0.40684 |  |
