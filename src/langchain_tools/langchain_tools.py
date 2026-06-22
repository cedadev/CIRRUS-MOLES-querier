from langchain_core.tools import tool as langchain_tool
from tool_functionality.search_catalogue import search_catalogue
from tool_functionality.get_record import get_record
from tool_functionality.search_redirect import search_redirect


@langchain_tool
def search_catalogue_tool(
    object_type=None, keywords=None, path=None, page=None, etc=None
):
    """Searches the MOLES catalogue using filters like keywords, object type and path.
    Use this tool when the user is looking for information. The responses are paginated, showing only up to the first 10 responses Which can be iterated through using page.
    observations (datasets), observation collections, computations, instruments, projects and platforms.

    Args:
        object_type (str, optional): The type of catalogue object to filter by (e.g., observations (datasets), observation collections, computations, instruments, projects and platforms).
        keywords (str, optional): Free-text keywords or search terms to match against the title and abstract.
        path (str, optional): A specific directory or catalogue path to narrow down the search.
        page (int, optional): The page number for paginated search results.
        etc (str, optional): Additional catch-all search parameters.
    """

    return search_catalogue(object_type, keywords, path, page, etc)


@langchain_tool
def get_record_tool(UUID: str = None, URL: str = None) -> dict:
    """
    Get the complete metadata record for a CEDA catalogue entry.

    Use this tool when the user provides a record UUID, a catalogue URL or wants more information about a dataset returned by another tool and
    wants detailed information about that specific record. The tool identifies
    the record type automatically and returns all available metadata fields.
    This tool excludes all top level values that are null, "" or [] (null, empty or empty lists), if a user asks about something that was not found in the returned record, assume it was one of the removed values.

    The input values are both optional, however, one of them must be filled. If both are filled, the UUID field only will be used

    Inputs:
        UUID (str, optional): Record UUID.
        URL (str, optional): Catalogue URL containing the UUID.

    Output:
        A dictionary of detailed record metadata.
    """

    return get_record(UUID, URL)


@langchain_tool
def search_redirect_tool(query: str) -> str:
    """
    Create a Google Custom Search link for a user query.

    This tool does not perform a search. It only generates a URL that the
    user can open to view search results. Use this tool if a direct search fails or if a user provides an old, ambiguous or out of scope (such as help pages) query that needs resolving.
    This will search the custom Google search engine across all CEDA searches.

    Input:
        A natural-language search query.

    Output:
        A valid Google Custom Search URL as a string.
    """

    return search_redirect(query)
