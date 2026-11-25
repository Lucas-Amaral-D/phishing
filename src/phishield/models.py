"""Configurações basais e espaço de busca com orçamento fixo."""
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

SEED = 42
SEARCH = {
    "logistica": {"C": [.1, 1, 10], "class_weight": [None, "balanced"]},
    "arvore": {"max_depth": [8, 16, None], "min_samples_leaf": [3, 15],
               "criterion": ["gini", "entropy"]},
    "floresta": {"max_depth": [12, 24, None], "min_samples_leaf": [2, 8],
                 "max_features": ["sqrt", "log2"], "class_weight": [None, "balanced"]},
    "boosting": {"learning_rate": [.05, .12], "max_leaf_nodes": [15, 31, 63],
                 "min_samples_leaf": [20, 50], "l2_regularization": [0., .5]},
}


def models():
    return {
        "dummy": DummyClassifier(strategy="prior"),
        "logistica": LogisticRegression(max_iter=350, random_state=SEED),
        "arvore": DecisionTreeClassifier(max_depth=16, min_samples_leaf=4, random_state=SEED),
        "floresta": RandomForestClassifier(
            n_estimators=24, min_samples_leaf=2, max_depth=22, n_jobs=4, random_state=SEED,
        ),
        "boosting": HistGradientBoostingClassifier(
            max_iter=90, early_stopping=False, random_state=SEED,
        ),
        "naive_bayes": GaussianNB(),
    }
