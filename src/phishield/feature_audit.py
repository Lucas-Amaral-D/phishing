"""Cenários e conjunto de atributos compartilhado pelos experimentos."""
import pandas as pd

from .data_validation import COLUMNS, TEXT_COLUMNS
from .feature_extraction import extract_url

UNCERTAIN = {
    "URLSimilarityIndex", "CharContinuationRate", "URLCharProb", "TLDLegitimateProb",
    "URLTitleMatchScore", "DomainTitleMatchScore",
}


def scenario_features(frame):
    lexical = pd.DataFrame.from_records(map(extract_url, frame.URL), index=frame.index)
    controlled = [column for column in COLUMNS if column not in TEXT_COLUMNS | UNCERTAIN | {"label"}]
    comprehensive = [*controlled, *sorted(UNCERTAIN), "TLD"]
    return {"A": frame[comprehensive], "B": frame[controlled], "C": lexical}
