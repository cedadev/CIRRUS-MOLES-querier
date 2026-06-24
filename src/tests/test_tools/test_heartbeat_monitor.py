from tool_functionality.heartbeat_monitor import check_services
import requests

class MockSuccessResponse():
    def __init__(self):
        self.status_code = 200

class MockFailResponse():
    def __init__(self):
        self.status_code = 500


def test_heartbeat_both_online(monkeypatch):
    def mock_get(type, timeout):
        if type == "https://api.catalogue.ceda.ac.uk/api/v3/":
            return MockSuccessResponse()
        if type == "http://localhost:11434":
            return MockSuccessResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    result = check_services()
    assert result == {"api_online": True, "ollama_online": True}

def test_heartbeat_both_offline(monkeypatch):
    def mock_get(type, timeout):
        if type == "https://api.catalogue.ceda.ac.uk/api/v3/":
            return MockFailResponse()
        if type == "http://localhost:11434":
            return MockFailResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    result = check_services()
    assert result == {"api_online": False, "ollama_online": False}

def test_heartbeat_ollama_online_only(monkeypatch):
    def mock_get(type, timeout):
        if type == "https://api.catalogue.ceda.ac.uk/api/v3/":
            return MockFailResponse()
        if type == "http://localhost:11434":
            return MockSuccessResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    result = check_services()
    assert result == {"api_online": False, "ollama_online": True}

def test_heartbeat_api_online_only(monkeypatch):
    def mock_get(type, timeout):
        if type == "https://api.catalogue.ceda.ac.uk/api/v3/":
            return MockSuccessResponse()
        if type == "http://localhost:11434":
            return MockFailResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    result = check_services()
    assert result == {"api_online": True, "ollama_online": False}
