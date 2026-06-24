from tool_functionality.search_redirect import search_redirect


def test_search_redirect_success():
    query = "big long string & has complicated things in! %$?"
    response = search_redirect(query)
    assert (
        response
        == "https://cse.google.com/cse?cx=009617667314646343139:y6z_ljohx30#gsc.tab=0&gsc.q=big+long+string+%26+has+complicated+things+in%21+%25%24%3F"
    )


def test_search_redirect_nonetype_query():
    response = search_redirect(None)
    assert response == "Query must not be a None type"


def test_search_redirect_unresponsive_link(monkeypatch):
    def mock_check_link(url):
        return "unresponsive"

    monkeypatch.setattr(
        "tool_functionality.search_redirect.check_link", mock_check_link
    )
    query = "bad search"
    response = search_redirect(query)
    assert (
        "Search Redirect Tool failed to create a valid link. This may be because the search is offline. The user can try to search the link and see if it works. link: https://cse.google.com/cse?cx=009617667314646343139:y6z_ljohx30#gsc.tab=0&gsc.q=bad+search"
        == response
    )
