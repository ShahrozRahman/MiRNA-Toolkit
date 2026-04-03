def combine_prediction_scores(scores: dict[str, float], weights: dict[str, float] | None = None) -> float:
    """Combine heterogeneous prediction scores into a confidence metric in [0, 1]."""
    if not scores:
        return 0.0

    if weights is None:
        weights = {name: 1.0 for name in scores}

    weighted_sum = 0.0
    total_weight = 0.0
    for name, value in scores.items():
        weight = weights.get(name, 1.0)
        weighted_sum += max(0.0, min(1.0, value)) * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0
    return weighted_sum / total_weight
