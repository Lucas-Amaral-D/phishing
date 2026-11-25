"""Inspeção estrutural de CSV em fluxo e validação da edição UCI 967."""

import csv
import math
from collections import Counter
from pathlib import Path

from .config import EXPECTED_COUNTS, INTERNAL_CLASSES

COLUMNS = tuple("""
FILENAME URL URLLength Domain DomainLength IsDomainIP TLD URLSimilarityIndex
CharContinuationRate TLDLegitimateProb URLCharProb TLDLength NoOfSubDomain HasObfuscation
NoOfObfuscatedChar ObfuscationRatio NoOfLettersInURL LetterRatioInURL NoOfDegitsInURL
DegitRatioInURL NoOfEqualsInURL NoOfQMarkInURL NoOfAmpersandInURL NoOfOtherSpecialCharsInURL
SpacialCharRatioInURL IsHTTPS LineOfCode LargestLineLength HasTitle Title DomainTitleMatchScore
URLTitleMatchScore HasFavicon Robots IsResponsive NoOfURLRedirect NoOfSelfRedirect HasDescription
NoOfPopup NoOfiFrame HasExternalFormSubmit HasSocialNet HasSubmitButton HasHiddenFields
HasPasswordField Bank Pay Crypto HasCopyrightInfo NoOfImage NoOfCSS NoOfJS NoOfSelfRef
NoOfEmptyRef NoOfExternalRef label
""".split())
TEXT_COLUMNS = {"FILENAME", "URL", "Domain", "TLD", "Title"}


def encode_target(original: str) -> int:
    """Converte o rótulo UCI em classe interna, com phishing positivo."""
    try:
        return INTERNAL_CLASSES[original]
    except KeyError:
        raise ValueError("Rótulo UCI inválido. Esperado 0 ou 1.") from None


def _type_rank(value: str) -> int:
    if not value.strip():
        return 0
    try:
        int(value)
        return 1
    except ValueError:
        try:
            return 2 if math.isfinite(float(value)) else 3
        except ValueError:
            return 3


def inspect_csv(path: Path) -> dict:
    """Conta registros e infere tipos sem expor valores de URLs ou títulos."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        columns = next(reader, [])
        if not columns or len(set(columns)) != len(columns):
            raise ValueError("Cabeçalho vazio ou com colunas duplicadas.")
        target = next((name for name in ("label", "Result") if name in columns), None)
        target_index = columns.index(target) if target else None
        counts = Counter()
        ranks = [0] * len(columns)
        known_text = TEXT_COLUMNS.intersection(columns)
        indices = [i for i, name in enumerate(columns) if name not in known_text]
        rows = 0
        for rows, row in enumerate(reader, start=1):
            if len(row) != len(columns):
                raise ValueError(f"Número de campos inválido no registro {rows}.")
            if target_index is not None:
                counts[row[target_index]] += 1
            for i in indices:
                if ranks[i] < 3:
                    ranks[i] = max(ranks[i], _type_rank(row[i]))
    names = ("vazio", "inteiro", "real", "texto")
    return {
        "rows": rows,
        "column_count": len(columns),
        "columns": columns,
        "types": {
            name: "texto" if name in known_text else names[rank]
            for name, rank in zip(columns, ranks, strict=True)
        },
        "target": target,
        "target_counts": dict(counts),
    }


def validate_phiusiil(summary: dict) -> None:
    """Exige o cabeçalho observado, a cardinalidade e as classes catalogadas."""
    if tuple(summary["columns"]) != COLUMNS:
        raise ValueError("Cabeçalho incompatível com o CSV oficial do PhiUSIIL.")
    if summary["rows"] != sum(EXPECTED_COUNTS.values()):
        raise ValueError("Quantidade de registros incompatível com a edição UCI 967.")
    if summary["target"] != "label" or summary["target_counts"] != EXPECTED_COUNTS:
        raise ValueError("Alvo ou distribuição de classes incompatível com a edição UCI 967.")
    invalid = [
        name for name in COLUMNS
        if name not in TEXT_COLUMNS and summary["types"][name] not in {"inteiro", "real"}
    ]
    if invalid:
        raise ValueError(f"Colunas numéricas com tipo incompatível: {', '.join(invalid)}.")
