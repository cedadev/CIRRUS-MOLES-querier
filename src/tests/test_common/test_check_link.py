from tool_functionality.common import check_link
import requests

"""
responsive
out_of_range
unresponsive
"""

def test_check_link_success(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200

    def mock_requests(url, timeout=None):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_requests)

    response = check_link("https://test_url/testing/success")
    assert response == "responsive"


def test_check_link_out_of_range(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 404

    def mock_requests(url, timeout=None):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_requests)

    response = check_link("https://test_url/testing/out-of-range")
    assert response == "out_of_range"


def test_check_link_unresponsive(monkeypatch):
    def mock_requests_fail(url, timeout=None):
        raise requests.exceptions.RequestException("Connection timed out or failed")

    monkeypatch.setattr(requests, "get", mock_requests_fail)

    response = check_link("https://test_url/testing/unresponsive")
    assert response == "unresponsive"
