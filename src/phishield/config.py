"""Caminhos e identidade catalogada das fontes."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
CATALOG = "https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset"
UCI_ZIP = "https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip"
UCI_CSV = "PhiUSIIL_Phishing_URL_Dataset.csv"
UCI_CSV_SHA256 = "a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6"
UCI_ZIP_SHA256 = "0a639fd03aea6308c5b1c10c92aa23c2ce1505447a9137271865cd0badc9a59a"
KAGGLE_ID = "akashkr/phishing-website-dataset"
EXPECTED_COUNTS = {"0": 100_945, "1": 134_850}
ORIGINAL_CLASSES = {"0": "phishing", "1": "legítimo"}
INTERNAL_CLASSES = {"0": 1, "1": 0}
DOI = "https://doi.org/10.1016/j.cose.2023.103545"
MENDELEY = "https://data.mendeley.com/datasets/shwpxscxy2/2"
EXPERIMENT = json.loads((ROOT / "configs/experiment_config.json").read_text(encoding="utf-8"))
