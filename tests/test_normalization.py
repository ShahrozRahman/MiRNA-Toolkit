from mirna_toolkit.quantification.normalization import rpm, tpm


def test_rpm_sums_to_one_million():
    values = rpm({"a": 50, "b": 50})
    assert round(sum(values.values()), 6) == 1_000_000.0


def test_tpm_zero_safe():
    values = tpm({"a": 0, "b": 0})
    assert values["a"] == 0.0
    assert values["b"] == 0.0
