import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from web2json.postprocessor import PostProcessor


def test_postprocessor_recovers_url_on_invalid_json():
    preprocessed = "download ftp://example.com/file.txt"
    pp = PostProcessor({"ftp_download": r"(ftp://\S+)"})
    result = pp.process("not json", preprocessed)
    assert result == {"ftp_download": "ftp://example.com/file.txt"}
