from typing import Any


def benchmark_classifiers(x, y, cv: int = 5) -> dict[str, float]:
    """Benchmark common classifiers for disease vs healthy tasks."""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_score
    except ImportError as exc:
        raise ImportError("scikit-learn is required for ML utilities. Install with: pip install mirna-toolkit[full]") from exc

    models: dict[str, Any] = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=42),
    }

    scores: dict[str, float] = {}
    for name, model in models.items():
        cv_scores = cross_val_score(model, x, y, cv=cv)
        scores[name] = float(cv_scores.mean())
    return scores
