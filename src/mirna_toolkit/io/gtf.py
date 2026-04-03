from dataclasses import dataclass
from pathlib import Path


@dataclass
class GtfRow:
    seqname: str
    source: str
    feature: str
    start: int
    end: int
    score: str
    strand: str
    frame: str
    attributes: str


def parse_gtf(path: str | Path) -> list[GtfRow]:
    rows: list[GtfRow] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) != 9:
                continue
            rows.append(
                GtfRow(
                    seqname=fields[0],
                    source=fields[1],
                    feature=fields[2],
                    start=int(fields[3]),
                    end=int(fields[4]),
                    score=fields[5],
                    strand=fields[6],
                    frame=fields[7],
                    attributes=fields[8],
                )
            )
    return rows
