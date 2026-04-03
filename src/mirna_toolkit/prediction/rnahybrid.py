def estimate_binding_energy(mirna_sequence: str, mrna_utr_sequence: str) -> float:
    """Estimate interaction energy proxy (more negative suggests stronger binding)."""
    mirna = mirna_sequence.upper().replace("T", "U")
    mrna = mrna_utr_sequence.upper().replace("T", "U")

    wc_pairs = {("A", "U"), ("U", "A"), ("G", "C"), ("C", "G")}
    wobble_pairs = {("G", "U"), ("U", "G")}

    score = 0.0
    for a, b in zip(mirna, mrna[::-1]):
        if (a, b) in wc_pairs:
            score -= 2.0
        elif (a, b) in wobble_pairs:
            score -= 1.0
    return score
