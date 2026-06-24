from langchain_core.tools import tool as langchain_tool
from tool_functionality.search_catalogue import search_catalogue
from tool_functionality.get_record import get_record
from tool_functionality.search_redirect import search_redirect


@langchain_tool
def search_catalogue_tool(
    object_type: str,
    title: str = None,
    abstract: str = None,
    keywords: str = None,
    path: str = None,
    creationDate: str = None,
    lastUpdatedDate: str = None,
    updateFrequency: str = None,
    dataLineage: str = None,
    publicationState: str = None,
    status: str = None,
    doiPublishedTime: str = None,
    instrumentType: str = None,
    platformType: str = None,
    timePeriodStart: str = None,
    timePeriodEnd: str = None,
    oldDataPath: list = None,
    page: int = 1,
    **kwargs
) -> dict:
    """
    Search the MOLES metadata catalogue for observations (could be referred to as datasets), computations, instruments, projects, platforms, observation collections (could be referred to as dataset collections)

    Use this tool when a user is searching for record information
    within the CEDA/MOLES catalogue. The tool supports heavy filtering and returns paginated results (20 per page).

    Args:
        object_type (str): REQUIRED. The category of object to search for. Must be one of: 
            'observations', 'computations', 'instruments', 'projects', 'platforms', 'observationcollections'.
        title (str, optional): Case-insensitive partial match string for the title.
        abstract (str, optional): Case-insensitive partial match string for the summary/abstract.
        keywords (str, optional): Keywords or tags associated with the dataset. This is a specific keyword search, for searching for substrings, use the title or abstract
        path (str, optional): The directory or catalogue path prefix (e.g., '/neodc/sister).
        creationDate (str, optional): Date the record was created (e.g., '2022-07-22').
        lastUpdatedDate (str, optional): Date the record was last modified.
        status (str, optional): Operational status (e.g., 'completed', 'superseded').
        instrumentType (str, optional): Filter by scientific instrument type used (will only work for instrument object type).
        platformType (str, optional): Filter by platform type (e.g., 'satellite') (will only work for platform object type).
        timePeriodStart (str, optional): Start window for the temporal coverage of data.
        timePeriodEnd (str, optional): End window for the temporal coverage of data.
        updateFrequency (str, optional): (e.g: 'notPlanned')
        dataLineage (str, optional): search for where the data may have come from using case-insensitive partial match string
        publicationState (str, optional): e.g: 'published'
        doiPublishedTime (str, optional): when a DOI was published (e.g., '2022-07-22'). This may be a null value for many records if they don't have a DOI
        oldDataPath (list, optional): a list type with a number in. Very few records have this value
        page (int, optional): The page number for pagination. Defaults to 1.
        kwargs (dict, optional): Additional catch-all search parameters.

    Returns:
        dict: A dictionary containing the paginated and filtered API response with the full number of records as metadata with a verified url_list
        linking directly to the CEDA catalogue page.
    """

    return search_catalogue(
        object_type,
        title,
        abstract,
        keywords,
        path,
        creationDate,
        lastUpdatedDate,
        updateFrequency,
        dataLineage,
        publicationState,
        status,
        doiPublishedTime,
        instrumentType,
        platformType,
        timePeriodStart,
        timePeriodEnd,
        oldDataPath,
        page,
        **kwargs
    )


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

    You should also give a brief explanation for why you are redirecting the user.

    Input:
        A natural-language search query.

    Output:
        A valid Google Custom Search URL as a string.
    """

    return search_redirect(query)
