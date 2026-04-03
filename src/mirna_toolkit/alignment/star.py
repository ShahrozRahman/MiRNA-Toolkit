import subprocess
from pathlib import Path


def align(
    fastq_path: str | Path,
    reference: str | Path,
    output_bam: str | Path | None = None,
    threads: int = 4,
    small_rna_mode: bool = True,
) -> Path:
    """Align reads with STAR in small-RNA-friendly settings and return BAM path."""
    fastq = Path(fastq_path)
    output = Path(output_bam) if output_bam else fastq.with_suffix(".star.bam")
    prefix = output.with_suffix("")

    cmd = [
        "STAR",
        "--genomeDir",
        str(reference),
        "--readFilesIn",
        str(fastq),
        "--runThreadN",
        str(threads),
        "--outSAMtype",
        "BAM",
        "Unsorted",
        "--outFileNamePrefix",
        f"{prefix}",
    ]
    if small_rna_mode:
        cmd.extend(["--alignIntronMax", "1", "--outFilterMismatchNmax", "1"])

    subprocess.run(cmd, check=True)
    produced_bam = Path(f"{prefix}Aligned.out.bam")
    produced_bam.replace(output)
    return output
