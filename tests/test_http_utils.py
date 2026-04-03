import requests

from mirna_toolkit.utils.http import safe_get_json


class _OkResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"ok": True}


class _FailResponse:
    def raise_for_status(self):
        raise requests.HTTPError("bad")


class _FakeSession:
    def __init__(self, response):
        self._response = response

    def get(self, *args, **kwargs):
        return self._response


def test_safe_get_json_returns_payload():
    payload = safe_get_json("https://example.org", session=_FakeSession(_OkResponse()))
    assert payload == {"ok": True}


def test_safe_get_json_non_strict_returns_none_on_error():
    payload = safe_get_json("https://example.org", strict=False, session=_FakeSession(_FailResponse()))
    assert payload is None
