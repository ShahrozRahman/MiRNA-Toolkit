from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_USER_AGENT = "miRNA-Toolkit/0.1.0"


def build_session(total_retries: int = 3, backoff_factor: float = 0.5) -> requests.Session:
    retry = Retry(
        total=total_retries,
        connect=total_retries,
        read=total_retries,
        status=total_retries,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        backoff_factor=backoff_factor,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    return session


def safe_get_json(
    url: str,
    params: dict[str, Any] | None = None,
    timeout: int = 60,
    strict: bool = False,
    session: requests.Session | None = None,
) -> Any:
    own_session = session is None
    sess = session if session is not None else build_session()

    try:
        response = sess.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        if strict:
            raise
        return None
    finally:
        if own_session:
            sess.close()


def download_file(
    url: str,
    output_path: str | Path,
    timeout: int = 60,
    strict: bool = True,
    session: requests.Session | None = None,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    own_session = session is None
    sess = session if session is not None else build_session()

    try:
        response = sess.get(url, timeout=timeout)
        response.raise_for_status()
        output.write_bytes(response.content)
    except requests.RequestException:
        if strict:
            raise
    finally:
        if own_session:
            sess.close()

    return output
