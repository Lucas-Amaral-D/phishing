"""Análise detalhada restrita aos registros de desenvolvimento."""
import json

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .config import ROOT  # noqa: E402
from .splitting import load_rows  # noqa: E402


def run_eda():
    output = ROOT / "results" / "exploracao"
    output.mkdir(parents=True, exist_ok=True)
    frame = load_rows("dev")
    numeric = frame.select_dtypes("number")
    text = frame.select_dtypes(exclude="number")
    unique = frame.nunique()
    summary = {
        "dimensions": list(frame.shape),
        "memory_bytes": int(frame.memory_usage(deep=True).sum()),
        "nulls": frame.isna().sum().to_dict(),
        "empty_strings": text.apply(lambda col: col.str.strip().eq("").sum()).to_dict(),
        "infinite": np.isinf(numeric).sum().to_dict(),
        "negative_values": numeric.lt(0).sum().to_dict(),
        "distinct": unique.to_dict(),
        "binary": [name for name in numeric if set(numeric[name].unique()) == {0, 1}],
        "constant": unique[unique <= 1].index.tolist(),
        "dominant_99_percent": [
            name for name in frame if frame[name].value_counts(normalize=True).iloc[0] >= .99
        ],
        "original_labels": frame.label.value_counts().to_dict(),
    }
    descriptive = numeric.describe().T
    descriptive["variance"] = numeric.var()
    descriptive["iqr"] = descriptive["75%"] - descriptive["25%"]
    descriptive["skew"] = numeric.skew()
    descriptive["outside_1_5_iqr"] = (
        numeric.lt(descriptive["25%"] - 1.5 * descriptive.iqr) |
        numeric.gt(descriptive["75%"] + 1.5 * descriptive.iqr)
    ).sum()
    descriptive.to_csv(output / "descritivas.csv")
    numeric.groupby("label").agg(["mean", "median", "std"]).T.to_csv(output / "por_classe.csv")
    correlation = numeric.corr()
    correlation.to_csv(output / "correlacao.csv")
    freq = frame.TLD.value_counts().rename("n").to_frame()
    freq["proporcao"] = freq.n / len(frame)
    freq.to_csv(output / "tld.csv")
    summary["domain_frequency"] = frame.Domain.value_counts().describe().to_dict()
    (output / "qualidade.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(2, 3, figsize=(14, 8), layout="constrained")
    by_class = [frame.loc[frame.label.eq(value), "URLLength"] for value in [0, 1]]
    names = ["Phishing", "Legítimo"]
    axes[0, 0].bar(names, [len(values) for values in by_class], color=["#a3344a", "#25685e"])
    axes[0, 0].set(title="Classes no desenvolvimento", ylabel="Registros")
    for name, values in zip(names, by_class, strict=True):
        axes[0, 1].hist(values, bins=np.arange(0, 302, 10), density=True, alpha=.55, label=name)
    axes[0, 1].set(title="Comprimento de URL até 300 caracteres", xlabel="Caracteres")
    axes[0, 1].legend()
    axes[0, 2].boxplot(by_class, tick_labels=names, showfliers=False)
    axes[0, 2].set(title="Comprimento de URL por classe", ylabel="Caracteres")
    columns = ["URLLength", "IsHTTPS", "URLSimilarityIndex", "TLDLegitimateProb", "label"]
    heat = axes[1, 0].imshow(correlation.loc[columns, columns], vmin=-1, vmax=1, cmap="coolwarm")
    short = ["Tam. URL", "HTTPS", "Similar.", "Prob. TLD", "Rótulo"]
    axes[1, 0].set(xticks=range(5), xticklabels=short, yticks=range(5), yticklabels=short,
                   title="Correlação de Pearson")
    fig.colorbar(heat, ax=axes[1, 0])
    freq.n.head(8).sort_values().plot.barh(ax=axes[1, 1], color="#25685e")
    axes[1, 1].set(title="Sufixos mais frequentes", xlabel="Registros", ylabel="Sufixo")
    frame.groupby("label")[["IsHTTPS", "HasTitle", "HasFavicon"]].mean().T.plot.bar(
        ax=axes[1, 2], rot=0, color=["#a3344a", "#25685e"]
    )
    axes[1, 2].legend(names)
    axes[1, 2].set(title="Características estruturais", ylabel="Proporção por classe")
    fig.savefig(output / "painel.png", dpi=180)
    plt.close(fig)
    return summary
