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
def get_record_tool(UUID=None, URL=None, session_number=None):
    """Retrieves full, detailed information for a specific MOLES record using an identifier.
    Use this tool when you already have a unique identifier (like a UUID or URL) for a record.

    Args:
        UUID (str, optional): The unique identifier (UUID) of the record to retrieve.
        URL (str, optional): The direct URL of the metadata record.
        session_number (int, optional): An optional session identifier if tracking historical states.
    """

    return get_record(UUID, URL, session_number)


@langchain_tool
def search_redirect_tool(query=None):
    """Use this tool if a direct search fails or if a user provides an old or ambiguous query that needs resolving.
    This will search the custom Google search engine across all CEDA searches. (this will return an external link)

    Args:
        query (str, optional): The raw search query or legacy string to check for redirects.
    """

    return search_redirect(query)
