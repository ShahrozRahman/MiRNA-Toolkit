from mirna_toolkit.quantification.novel import discover_novel_mirnas


def test_discover_novel_mirnas(tmp_path):
    fasta = tmp_path / "collapsed.fa"
    fasta.write_text(">read1_x20\nAUGCUAGCUAGCUAGCUAGC\n>read2_x2\nAUGCUA\n", encoding="utf-8")
    candidates = discover_novel_mirnas(fasta, min_count=10)
    assert len(candidates) == 1
    assert candidates[0]["read_count"] == 20
