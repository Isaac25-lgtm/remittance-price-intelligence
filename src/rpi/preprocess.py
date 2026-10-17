"""Immutable raw workbook -> typed, provenance-tagged service-quote table."""
from __future__ import annotations

import re
from datetime import datetime
import unicodedata

import numpy as np
import pandas as pd

from . import config

RAW_COLUMNS = [
    "id", "period", "source_code", "source_name", "source_region", "source_income",
    "source_lending", "source_G8G20", "destination_code", "destination_name",
    "destination_region", "destination_income", "destination_lending", "destination_G8G20",
    "firm", "firm_type", "payment instrument", "access point", "speed actual",
    "cc1 lcu amount", "cc1 denomination amount", "cc1 lcu code", "cc1 lcu fee",
    "cc1 lcu fx rate", "cc1 fx margin", "cc1 total cost %", "cc2 lcu amount",
    "cc2 denomination amount", "cc2 lcu code", "cc2 lcu fee", "cc2 lcu fx rate",
    "cc2 fx margin", "cc2 total cost %", "inter lcu bank fx", "transparent", "Standard Note",
    "note2", "receiving network coverage", "pickup location", "pickup method", "date", "corridor",
]

NUMERIC = [
    "cc1 lcu amount", "cc1 denomination amount", "cc1 lcu fee", "cc1 lcu fx rate",
    "cc1 fx margin", "cc1 total cost %", "cc2 lcu amount", "cc2 denomination amount",
    "cc2 lcu fee", "cc2 lcu fx rate", "cc2 fx margin", "cc2 total cost %", "inter lcu bank fx",
]

IDENTITY_TEXT = [
    "firm", "firm_type", "payment instrument", "access point", "speed actual",
    "receiving network coverage", "pickup location", "pickup method", "transparent",
]

_PERIOD_RE = re.compile(r"^(\d{4})_([1-4])Q$")


def parse_period(p: str) -> tuple[int, int]:
    """'2016_2Q' -> (2016, 2). Raises on any other format (no silent coercion)."""
    m = _PERIOD_RE.match(str(p).strip())
    if not m:
        raise ValueError(f"unparseable period: {p!r}")
    return int(m.group(1)), int(m.group(2))


def quarter_index(year: int, q: int) -> int:
    """Consecutive integer index: adjacent calendar quarters differ by exactly 1."""
    return year * 4 + (q - 1)


def qlabel(qidx: int) -> str:
    return f"{qidx // 4}Q{qidx % 4 + 1}"


def parse_date(x):
    """Collection date: published as 'dd/Mon/yyyy' text, or as an Excel datetime (2025Q3)."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return pd.NaT
    if isinstance(x, (pd.Timestamp, datetime)):
        return pd.Timestamp(x)
    return pd.to_datetime(str(x).strip(), format="%d/%b/%Y", errors="coerce")


def norm_text(x) -> str:
    """Deterministic, conservative normalisation: NFKC, casefold, collapse whitespace,
    normalise separators. No fuzzy matching; distinct strings stay distinct otherwise."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    s = unicodedata.normalize("NFKC", str(x)).casefold().strip()
    s = re.sub(r"\s*,\s*", ",", s)
    s = re.sub(r"\s+", " ", s)
    return s


def read_raw_sheet(path=config.RAW_FILE) -> pd.DataFrame:
    """Read the post-Q2-2016 sheet exactly as published (all named columns as object)."""
    df = pd.read_excel(path, sheet_name=config.SHEET_POST2016, header=0,
                       dtype=object, engine="openpyxl")
    extra = df.columns[config.N_NAMED_COLUMNS_POST2016:]
    n_nonempty_extra = int(df[extra].notna().sum().sum())
    df = df.iloc[:, : config.N_NAMED_COLUMNS_POST2016].copy()
    if list(df.columns) != RAW_COLUMNS:
        raise ValueError(f"schema drift: {list(df.columns)}")
    df.attrs["n_nonempty_extra_cells"] = n_nonempty_extra
    df.attrs["n_columns_read"] = config.N_NAMED_COLUMNS_POST2016 + len(extra)
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Typed copy with provenance. Raw values are preserved in *_raw columns for numerics."""
    out = df.copy()
    out.insert(0, "source_row", np.arange(2, len(out) + 2))  # Excel row number
    yq = out["period"].map(parse_period)
    out["year"] = yq.map(lambda t: t[0]).astype(int)
    out["qtr"] = yq.map(lambda t: t[1]).astype(int)
    out["qidx"] = [quarter_index(y, q) for y, q in zip(out["year"], out["qtr"])]
    for c in NUMERIC:
        raw = out[c]
        num = pd.to_numeric(raw, errors="coerce")
        out[c + "__nonnumeric"] = raw.notna() & num.isna() & (raw.astype(str).str.strip() != "")
        out[c] = num.astype(float)
    for c in IDENTITY_TEXT:
        out[c + "__n"] = out[c].map(norm_text)
    out["collection_date"] = out["date"].map(parse_date)
    out["corridor_key"] = out["source_code"].astype(str) + ">" + out["destination_code"].astype(str)
    for c in ["source_code", "destination_code", "source_region", "destination_region",
              "source_income", "destination_income", "corridor", "period"]:
        out[c] = out[c].astype(str)
    return out


def load_clean(rebuild: bool = False) -> pd.DataFrame:
    """Cached typed table (data/processed is gitignored, never published)."""
    if config.CACHE_FILE.exists() and not rebuild:
        return pd.read_parquet(config.CACHE_FILE)
    raw = read_raw_sheet()
    print({"raw_rows": len(raw), **raw.attrs})
    df = clean(raw)
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    obj = [c for c in df.columns if df[c].dtype == object]
    df[obj] = df[obj].astype(str).where(df[obj].notna(), None)
    df.to_parquet(config.CACHE_FILE, index=False)
    return df
