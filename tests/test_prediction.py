from mirna_toolkit.prediction.confidence import combine_prediction_scores
from mirna_toolkit.prediction.seed_match import seed_match_score


def test_seed_match_binary_score():
    score = seed_match_score("AUGCAUACG", "TTTTGTATGCTTT")
    assert score in {0.0, 1.0}


def test_confidence_score_in_bounds():
    score = combine_prediction_scores({"seed": 1.0, "thermo": 0.7})
    assert 0.0 <= score <= 1.0
