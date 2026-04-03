from __future__ import annotations

from pathlib import Path

from ..utils.http import download_file

MIRBASE_BASE = "https://www.mirbase.org/ftp"
GEO_BASE = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi"
ENSEMBL_BASE = "https://ftp.ensembl.org/pub"


def _download(url: str, output_path: str | Path) -> Path:
    return download_file(url, output_path)


def download_mirbase_release(filename: str, output_dir: str | Path = "data") -> Path:
    output = Path(output_dir) / filename
    return _download(f"{MIRBASE_BASE}/{filename}", output)


def download_geo_series(gse_id: str, output_path: str | Path) -> Path:
    url = f"{GEO_BASE}?acc={gse_id}&targ=self&form=text&view=quick"
    return _download(url, output_path)


def download_ensembl_release(release_path: str, output_dir: str | Path = "data") -> Path:
    filename = Path(release_path).name
    output = Path(output_dir) / filename
    return _download(f"{ENSEMBL_BASE}/{release_path}", output)
