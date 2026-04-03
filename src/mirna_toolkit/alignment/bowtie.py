import subprocess
from pathlib import Path


def align(
    fastq_path: str | Path,
    reference: str | Path,
    output_bam: str | Path | None = None,
    threads: int = 4,
) -> Path:
    """Align reads with Bowtie and return BAM path."""
    fastq = Path(fastq_path)
    output = Path(output_bam) if output_bam else fastq.with_suffix(".bowtie.bam")
    sam = output.with_suffix(".sam")

    subprocess.run(
        ["bowtie", "-p", str(threads), "-S", str(reference), str(fastq), str(sam)],
        check=True,
    )
    subprocess.run(["samtools", "view", "-bS", str(sam), "-o", str(output)], check=True)
    return output
