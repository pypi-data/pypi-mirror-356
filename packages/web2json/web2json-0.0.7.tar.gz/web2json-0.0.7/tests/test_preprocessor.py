import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from web2json.preprocessor import BasicPreprocessor

class DummyResp:
    def __init__(self):
        self.encoding = None
        self.apparent_encoding = 'utf-8'
        self.text = 'OK'
        self.status_checked = False

    def raise_for_status(self):
        self.status_checked = True

def test_fetch_content_uses_apparent_encoding(monkeypatch):
    resp = DummyResp()

    def fake_get(url, headers=None, timeout=15):
        return resp

    monkeypatch.setattr(requests, "get", fake_get)
    pre = BasicPreprocessor()
    text = pre._fetch_content("http://example.com")
    assert text == 'OK'
    assert resp.encoding == 'utf-8'
    assert resp.status_checked

def test_fetch_content_error(monkeypatch):
    def fake_get(url, headers=None, timeout=15):
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", fake_get)
    pre = BasicPreprocessor()
    with pytest.raises(ValueError):
        pre._fetch_content("http://bad")
