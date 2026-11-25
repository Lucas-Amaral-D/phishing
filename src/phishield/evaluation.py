"""Métricas binárias com phishing como positivo."""
from sklearn.metrics import (
    accuracy_score, auc, average_precision_score, balanced_accuracy_score, confusion_matrix,
    f1_score, fbeta_score, matthews_corrcoef, precision_recall_curve, precision_score, recall_score,
    roc_auc_score,
)


def metrics(y, scores, threshold=.5):
    predicted = scores >= threshold
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel().tolist()
    precision, recall, _ = precision_recall_curve(y, scores)
    return {
        "accuracy": accuracy_score(y, predicted),
        "balanced_accuracy": balanced_accuracy_score(y, predicted),
        "precision": precision_score(y, predicted, zero_division=0),
        "recall": recall_score(y, predicted, zero_division=0),
        "specificity": tn / (tn + fp) if tn + fp else 0.,
        "f1": f1_score(y, predicted, zero_division=0),
        "f2": fbeta_score(y, predicted, beta=2, zero_division=0),
        "roc_auc": roc_auc_score(y, scores) if len(set(y)) == 2 else None,
        "average_precision": average_precision_score(y, scores) if tp + fn else None,
        "pr_auc_trapezoid": auc(recall, precision) if tp + fn else None,
        "mcc": matthews_corrcoef(y, predicted),
        "fpr": fp / (tn + fp) if tn + fp else 0.,
        "fnr": fn / (fn + tp) if fn + tp else 0.,
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
    }
