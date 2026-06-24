from tool_functionality.get_record import get_record


def test_get_record_success(monkeypatch):
    """
    Tests a successful run of the tool

    This tests the UUID and URL logic
    - if only UUID, uses that
    - if only URL, successfully extracts UUID and uses that
    - if using both, only use the UUID input

    Also tests the filtering logic
    - filters "", None and []
    - top level only

    tests short_code referencing as well
    """

    def mock_call_api(params, endpoint):
        if endpoint == "referenceables":
            return {"results": [{"short_code": "ob"}]}
        if endpoint == "observations":
            assert params["uuid"] == "794eccbedfb6b78471fd077a4e406ac2"
            return {
                "results": [
                    {
                        "title": "Dataset",
                        "information": [
                            "fact 1",
                            "fact 2",
                            [],
                        ],
                        "empty_field": "",
                        "null_field": None,
                        "list_field": [],
                    }
                ]
            }

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    response1 = get_record(UUID="794eccbedfb6b78471fd077a4e406ac2")
    assert response1 == {"title": "Dataset", "information": ["fact 1", "fact 2", []]}

    response2 = get_record(
        URL="https://catalogue.ceda.ac.uk/uuid/794eccbedfb6b78471fd077a4e406ac2/"
    )
    assert response2 == {"title": "Dataset", "information": ["fact 1", "fact 2", []]}

    response3 = get_record(
        UUID="794eccbedfb6b78471fd077a4e406ac2",
        URL="https://catalogue.ceda.ac.uk/uuid/12345678904fhdlj/",
    )
    assert response3 == {"title": "Dataset", "information": ["fact 1", "fact 2", []]}


def test_get_record_fail_no_uuid_or_url():
    response = get_record(UUID=None, URL=None)
    assert response == "You must enter a valid URL or UUID"


def test_get_record_fail_bad_url():
    response = get_record(URL="https://catalogue.ceda.ac.uk/bad-path/something_wierd")
    assert response == "You must enter a valid URL or UUID"


def test_get_record_fail_no_short_code(monkeypatch):
    def mock_call_api(params, endpoint):
        return {"results": []}

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    UUID = "missing-uuid"
    response = get_record(UUID=UUID)
    assert (
        response
        == f"Failed to get short code of UUID {UUID}. This may mean the UUID does not exist."
    )


def test_get_record_fail_unsuccessful_information_call(monkeypatch):
    def mock_call_api(params, endpoint):
        if endpoint == "referenceables":
            return {"results": [{"short_code": "ob"}]}
        if endpoint == "observations":
            return {"results": []}

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    UUID = "missing-uuid"
    response = get_record(UUID=UUID)
    assert (
        response
        == f"Failed to get data for UUID {UUID}. Reaching this far means the UUID exists within referencables and that was called successfully, so this is highly irregular (perhaps the API shut down between calls?)"
    )


def test_get_record_fail_bad_short_code(monkeypatch):
    def mock_call_api(params, endpoint):
        return {"results": [{"short_code": "egg"}]}

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    UUID = "normal-uuid"
    response = get_record(UUID=UUID)
    assert response == "Unknown API short code: egg"


def test_get_record_fail_API(monkeypatch):
    def mock_call_api(params, endpoint):
        return {
            "error": f"Request failed: RequestException",
            "params": {"param1": "thing1", "param2": "thing2"},
        }

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    error_response = {
        "error": f"Request failed: RequestException",
        "params": {"param1": "thing1", "param2": "thing2"},
    }

    UUID = "normal-uuid"
    response = get_record(UUID=UUID)
    assert (
        response
        == f"An error occurred While trying to get the short code of UUID {UUID}. This may mean the UUID does not exist. Error: {error_response}"
    )


def test_get_record_fail_API_2(monkeypatch):
    def mock_call_api(params, endpoint):
        if endpoint == "referenceables":
            return {"results": [{"short_code": "ob"}]}
        if endpoint == "observations":
            return {
                "error": f"Request failed: RequestException",
                "params": {"param1": "thing1", "param2": "thing2"},
            }

    monkeypatch.setattr("tool_functionality.get_record.call_api", mock_call_api)

    error_response = {
        "error": f"Request failed: RequestException",
        "params": {"param1": "thing1", "param2": "thing2"},
    }

    UUID = "normal-uuid"
    response = get_record(UUID=UUID)
    assert response == f"API Error fetching information: {error_response}"
