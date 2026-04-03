def seed_match_score(mirna_sequence: str, mrna_utr_sequence: str) -> float:
    """Return a seed match score in [0, 1] based on canonical 7mer seed presence."""
    if len(mirna_sequence) < 8:
        return 0.0

    # Use positions 2-8 as canonical seed, reverse-complemented for target matching.
    seed = mirna_sequence[1:8].upper().replace("U", "T")
    comp = seed.translate(str.maketrans("ATCG", "TAGC"))[::-1]
    utr = mrna_utr_sequence.upper().replace("U", "T")

    return 1.0 if comp in utr else 0.0
