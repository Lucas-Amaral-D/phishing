"""Consolida métricas por fold e figuras sem reajustar modelos."""
import argparse
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def summarize(directory):
    comparison = pd.read_csv(directory / "comparacao.csv")
    records = []
    for row in comparison.itertuples():
        table = pd.read_csv(directory / f"{row.scenario}_{row.model}.csv")
        for column in table.columns[3:]:
            records.append({
                "scenario": row.scenario, "model": row.model, "metric": column,
                "mean": table[column].mean(), "sd": table[column].std(),
            })
    pd.DataFrame(records).to_csv(directory / "metricas_agregadas.csv", index=False)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout="constrained")
    for i, (scenario, table) in enumerate(comparison.groupby("scenario")):
        positions = [j + .23 * i for j in range(len(table))]
        if scenario == "A":
            continue
        axes[0].bar(positions, table.mean_f1, yerr=table.sd_f1, width=.22, label=scenario)
    baselines = comparison[comparison.scenario.eq("B")]
    axes[0].set(xticks=[i + .35 for i in range(len(baselines))], xticklabels=baselines.model,
                ylim=(0, 1.05), title="Baselines por cenário", ylabel="F1 médio da classe phishing")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend()
    grouped = comparison[comparison.model.eq("boosting")].set_index("scenario").mean_f1
    random = pd.Series({
        key: pd.read_csv(directory / f"{key}_aleatorio.csv").f1.mean() for key in "ABC"
    })
    table = pd.DataFrame({"Domínio": grouped, "Aleatório": random})
    table.to_csv(directory / "agrupado_vs_aleatorio.csv")
    table.plot.bar(ax=axes[1], rot=0, color=["#21564b", "#92743b"])
    axes[1].set(ylim=(.8, 1.005), xlabel="Cenário", ylabel="F1 médio", title="Boosting por partição")
    fig.savefig(directory / "comparacao.png", dpi=180)
    plt.close(fig)
    for key in "BC":
        threshold = pd.read_csv(directory / f"limiar_{key}.csv")
        learning = pd.read_csv(directory / f"aprendizado_{key}.csv")
        fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
        threshold.set_index("threshold")[["precision", "recall", "f1", "f2"]].plot(ax=axes[0])
        axes[0].set(xlabel="Limiar", ylabel="Métrica", title=f"Compromisso de limiar {key}")
        axes[1].plot(learning.rows, learning.f1, marker="o")
        axes[1].set(xlabel="Registros de treino", ylabel="F1", title=f"Curva de aprendizado {key}")
        fig.savefig(directory / f"curvas_{key}.png", dpi=180)
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    summarize(parser.parse_args().experiment)
