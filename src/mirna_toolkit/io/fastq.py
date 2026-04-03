from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FastqRecord:
    header: str
    sequence: str
    plus: str
    quality: str


def parse_fastq(path: str | Path):
    """Yield FASTQ records from a file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        while True:
            header = handle.readline().rstrip("\n")
            if not header:
                break
            sequence = handle.readline().rstrip("\n")
            plus = handle.readline().rstrip("\n")
            quality = handle.readline().rstrip("\n")
            if not quality:
                raise ValueError("Malformed FASTQ: incomplete record")
            yield FastqRecord(header=header, sequence=sequence, plus=plus, quality=quality)


def run_fastqc(fastq_path: str | Path, output_dir: str | Path) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    cmd = ["fastqc", str(fastq_path), "-o", str(output)]
    subprocess.run(cmd, check=True)
    return output


def trim_adapters(fastq_path: str | Path, output_fastq: str | Path, threads: int = 4) -> Path:
    out = Path(output_fastq)
    cmd = ["fastp", "-i", str(fastq_path), "-o", str(out), "-w", str(threads)]
    subprocess.run(cmd, check=True)
    return out
