from tool_functionality.common import call_api
import requests


def test_call_api_success(monkeypatch):
    expected = {"results": ["a", "b"]}

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return expected

    def mock_get(url, params, timeout):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = call_api({"uuid": "good-uuid"}, "referenceables")

    assert result == expected


def test_call_api_http_error(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError(
                "500 Server Error: Internal Server Error"
            )

    def mock_get(url, params, timeout):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = call_api({"uuid": "good-uuid"}, "referenceables")

    assert "error" in result
    assert "500 Server Error" in result["error"]


def test_call_api_timeout(monkeypatch):
    def mock_get(url, params, timeout):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr(requests, "get", mock_get)

    result = call_api({"uuid": "good-uuid"}, "referenceables")

    assert "error" in result
    assert "timed out" in result["error"]


def test_call_api_connection_error(monkeypatch):
    def mock_get(url, params, timeout):
        raise requests.exceptions.ConnectionError("Failed to establish connection")

    monkeypatch.setattr(requests, "get", mock_get)

    result = call_api({"uuid": "good-uuid"}, "referenceables")

    assert "error" in result
    assert "Failed to establish connection" in result["error"]


def test_call_api_invalid_json(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    def mock_get(url, params, timeout):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = call_api({"uuid": "good-uuid"}, "referenceables")

    assert "error" in result
    assert "Failed to parse JSON" in result["error"]
