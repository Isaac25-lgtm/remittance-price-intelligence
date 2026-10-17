"""Frozen paths and constants. Values here are the pre-registered analysis choices."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"

SOURCE_URL = (
    "https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095523/"
    "rpw_dataset_2011_2025_q3.xlsx"
)
CATALOGUE_URL = "https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide"
RAW_FILE = RAW_DIR / "rpw_dataset_2011_2025_q3.xlsx"
EXPECTED_SHA256 = "f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8"
EXPECTED_BYTES = 50_780_339
SHEET_POST2016 = "Dataset (from Q2 2016)"
N_NAMED_COLUMNS_POST2016 = 42  # remaining 32 columns are unnamed and empty (audited)
CACHE_FILE = PROCESSED_DIR / "rpw_post2016.parquet"

THRESHOLD = 3.0  # percent of transfer value (SDG 10.c reference level)
SECONDARY_THRESHOLD = 5.0
PRIMARY_BASKET = "cc1"  # USD 200 equivalent; cc2 (USD 500) is a separate product
SEED = 20261017

# East African Community membership (8 partner states as of 2024) used only for subgroup support.
EAST_AFRICA = ["BDI", "COD", "KEN", "RWA", "SOM", "SSD", "TZA", "UGA"]
