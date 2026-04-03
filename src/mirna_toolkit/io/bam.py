from __future__ import annotations

import subprocess
from pathlib import Path


def fastq_to_bam(
    fastq_path: str | Path,
    reference: str | Path,
    output_bam: str | Path,
    aligner: str = "bowtie",
) -> Path:
    """Convert FASTQ to BAM through selected aligner + samtools."""
    out = Path(output_bam)
    sam_path = out.with_suffix(".sam")

    if aligner == "bowtie":
        cmd = ["bowtie", "-S", str(reference), str(fastq_path), str(sam_path)]
    elif aligner == "hisat2":
        cmd = ["hisat2", "-x", str(reference), "-U", str(fastq_path), "-S", str(sam_path)]
    elif aligner == "star":
        cmd = ["STAR", "--genomeDir", str(reference), "--readFilesIn", str(fastq_path), "--outFileNamePrefix", str(sam_path.with_suffix(""))]
    else:
        raise ValueError("aligner must be one of: bowtie, hisat2, star")

    subprocess.run(cmd, check=True)
    subprocess.run(["samtools", "view", "-bS", str(sam_path), "-o", str(out)], check=True)
    return out


def bam_to_fasta(bam_path: str | Path, output_fasta: str | Path) -> Path:
    out = Path(output_fasta)
    subprocess.run(["samtools", "fasta", str(bam_path), "-o", str(out)], check=True)
    return out
