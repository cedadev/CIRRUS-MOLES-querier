from tool_functionality.search_catalogue import search_catalogue, get_object_type


def test_type_key_match():
    response = get_object_type("coll")
    assert response == "observationcollections"


def test_type_value_match():
    response = get_object_type("computations")
    assert response == "computations"


def test_type_substring_match():
    response = get_object_type("pro")
    assert response == "projects"


def test_type_no_match():
    response = get_object_type("egg")
    assert response == None


def test_search_catalogue_success(monkeypatch):
    def mock_call_api(params, api_type):
        assert params == {"page": 1, "title__icontains": "Map"}
        return {
            "results": [
                {
                    "uuid": "some-UUID",
                    "title": "Dataset",
                    "information": [
                        "fact 1",
                        "fact 2",
                        [],
                    ],
                    "empty_field": "",
                    "null_field": None,
                    "list_field": [],
                    "onlineresource_set": "stuff that should disappear",
                }
            ]
        }

    monkeypatch.setattr("tool_functionality.search_catalogue.call_api", mock_call_api)

    response = search_catalogue(object_type="ob", title="Map")
    assert response == {
        "response": {
            "results": [
                {
                    "uuid": "some-UUID",
                    "title": "Dataset",
                    "information": ["fact 1", "fact 2", []],
                    "empty_field": "",
                    "null_field": None,
                    "list_field": [],
                }
            ]
        },
        "verified_urls": ["https://catalogue.ceda.ac.uk/uuid/some-UUID/"],
    }


def test_search_catalogue_invalid_object_type():
    response = search_catalogue("egg")
    assert (
        response
        == "Invalid object type. This must be any value from 'short_code' within your system prompt"
    )


def test_search_catalogue_api_error(monkeypatch):
    def mock_call_api(params, api_type):
        return {
            "error": f"Request failed: RequestException",
            "params": {"param1": "thing1", "param2": "thing2"},
        }

    monkeypatch.setattr("tool_functionality.search_catalogue.call_api", mock_call_api)

    error_response = {
        "error": f"Request failed: RequestException",
        "params": {"param1": "thing1", "param2": "thing2"},
    }

    UUID = "normal-uuid"
    response = search_catalogue(UUID=UUID, object_type="observation")
    assert response == f"API Error fetching information: {error_response}"


def test_search_catalogue_bad_link(monkeypatch):
    def mock_call_api(params, api_type):
        return {
            "results": [
                {
                    "uuid": "some-UUID",
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

    def mock_check_link(url):
        return "unresponsive"

    monkeypatch.setattr(
        "tool_functionality.search_catalogue.check_link", mock_check_link
    )

    monkeypatch.setattr("tool_functionality.search_catalogue.call_api", mock_call_api)

    response = search_catalogue(object_type="ob", title="Map")
    assert response == {
        "response": {
            "results": [
                {
                    "uuid": "some-UUID",
                    "title": "Dataset",
                    "information": ["fact 1", "fact 2", []],
                    "empty_field": "",
                    "null_field": None,
                    "list_field": [],
                }
            ]
        },
        "verified_urls": ["Failed to create link for UUID: some-UUID"],
    }
