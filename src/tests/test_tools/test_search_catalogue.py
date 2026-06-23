from tool_functionality.search_catalogue import search_catalogue



"""
get_object_type:

direct key match
direct value match
substring match
no match


search_catalogue:

runs successfully (including url_list)
invalid object type
malformed kwargs
heavy field to filter out does not exist
link failed to be responsive
"""














def test_search_catalogue():
    pass





"""
def test_get_record_success(monkeypatch):
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
"""
