"""Frozen baseline and model ladder. All preprocessing is fit inside the training fold only."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, SplineTransformer, StandardScaler

from . import config
from .features import CATEGORICAL, NUMERIC, SPLINE_NUMERIC

OTHER_NUMERIC = [c for c in NUMERIC if c not in SPLINE_NUMERIC]


def _onehot():
    return OneHotEncoder(handle_unknown="ignore", min_frequency=20, sparse_output=False)


class ConstantModel:
    def __init__(self, p=None):
        self.p = p

    def fit(self, X, y):
        if self.p is None:
            self.p_ = float(np.mean(y))
        else:
            self.p_ = float(self.p)
        return self

    def predict_proba(self, X):
        p = np.full(len(X), self.p_)
        return np.column_stack([1 - p, p])


class ColumnProbability:
    """Uses a past-only history feature directly as the probability (no fitting)."""
    def __init__(self, col):
        self.col = col

    def fit(self, X, y):
        return self

    def predict_proba(self, X):
        p = np.clip(X[self.col].to_numpy(dtype=float), 1e-6, 1 - 1e-6)
        return np.column_stack([1 - p, p])


def ridge_logistic():
    pre = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), NUMERIC),
        ("cat", _onehot(), CATEGORICAL)])
    return Pipeline([("pre", pre), ("clf", LogisticRegression(C=1.0, max_iter=2000))])


def cost_logistic():
    pre = ColumnTransformer([("num", StandardScaler(), ["cost"])])
    return Pipeline([("pre", pre), ("clf", LogisticRegression(C=1.0, max_iter=1000))])


def spline_logistic():
    pre = ColumnTransformer([
        ("spl", make_pipeline(SimpleImputer(strategy="median"),
                              SplineTransformer(n_knots=5, degree=3, knots="quantile",
                                                extrapolation="constant")), SPLINE_NUMERIC),
        ("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()),
         OTHER_NUMERIC),
        ("cat", _onehot(), CATEGORICAL)])
    return Pipeline([("pre", pre), ("clf", LogisticRegression(C=1.0, max_iter=3000))])


def hist_gbm():
    pre = ColumnTransformer([
        ("num", "passthrough", NUMERIC),
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1,
                               encoded_missing_value=-1, min_frequency=20), CATEGORICAL)],
        verbose_feature_names_out=False)
    clf = HistGradientBoostingClassifier(
        learning_rate=0.05, max_iter=300, max_leaf_nodes=15, min_samples_leaf=50,
        l2_regularization=1.0, early_stopping=False, random_state=config.SEED,
        categorical_features=list(range(len(NUMERIC), len(NUMERIC) + len(CATEGORICAL))))
    return Pipeline([("pre", pre), ("clf", clf)])


def random_forest():
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median", add_indicator=True), NUMERIC),
        ("cat", _onehot(), CATEGORICAL)])
    clf = RandomForestClassifier(n_estimators=300, min_samples_leaf=20, max_features="sqrt",
                                 n_jobs=2, random_state=config.SEED)
    return Pipeline([("pre", pre), ("clf", clf)])


MODELS = {
    "B0_always_stay": lambda: ConstantModel(p=1.0 - 1e-6),
    "B1_prevalence": lambda: ConstantModel(),
    "B2_history": lambda: ColumnProbability("h_corrfirm"),
    "B3_cost_logistic": cost_logistic,
    "L1_ridge_logistic": ridge_logistic,
    "L2_spline_logistic": spline_logistic,
    "M1_hist_gbm": hist_gbm,
    "M2_random_forest": random_forest,
}
