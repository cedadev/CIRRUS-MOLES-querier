from .common import call_api, check_link, API_TYPES

STRIP_FIELDS = {
    "phenomena",
    "resultQuality",
    "identifier_set",
    "procedureCompositeProcess",
    "responsiblepartyinfo_set",
    "discoveryKeywords",
    "onlineresource_set",
}


def get_object_type(object_type):
    obj_type = object_type.strip().lower()

    # Direct key match
    for key in API_TYPES.keys():
        if obj_type in key:
            return API_TYPES[key]

    # Direct value match
    for value in API_TYPES.values():
        if value == obj_type:
            return value

    # substring match
    for value in API_TYPES.values():
        if obj_type in value:
            return value


def search_catalogue(
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
    **kwargs,
) -> dict:
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
    """
    Search the MOLES metadata catalogue for observations (could be referred to as datasets), computations, instruments, projects, platforms, observation collections (could be referred to as dataset collections)

    Use this tool when a user is searching for record information
    within the CEDA/MOLES catalogue. The tool supports heavy filtering and returns paginated results (20 per page).

    Args:
        object_type (str): REQUIRED. The category of object to search for. Must be one of: 
            'observations', 'computations', 'instruments', 'projects', 'platforms', 'observationcollections'.
        title (str, optional): Case-insensitive partial match string for the title.
        abstract (str, optional): Case-insensitive partial match string for the summary/abstract.
        keywords (str, optional): Keywords or tags associated with the dataset.
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

    Returns:
        dict: A dictionary containing the paginated and filtered API response with the full number of records as metadata with a verified url_list
        linking directly to the CEDA catalogue page.
    """
    obj_type = get_object_type(object_type)
    if not obj_type:
        return "Invalid object type. This must be any value from 'short_code' within your system prompt"

    params = {"page": page}

    icontains_fields = {
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "creationDate": creationDate,
        "lastUpdatedDate": lastUpdatedDate,
        "updateFrequency": updateFrequency,
        "dataLineage": dataLineage,
        "publicationState": publicationState,
        "status": status,
        "doiPublishedTime": doiPublishedTime,
        "instrumentType": instrumentType,
        "platformType": platformType,
    }

    # Add icontains if there are values
    for api_param, value in icontains_fields.items():
        if value:
            params[f"{api_param}__icontains"] = value

    # Non icontains filters
    if path:
        params["result_field__dataPath__startswith"] = path
    if timePeriodStart:
        params["timePeriod__startTime__startswith"] = timePeriodStart
    if timePeriodEnd:
        params["timePeriod__endTime__startswith"] = timePeriodEnd
    if oldDataPath:
        params["result_field__oldDataPath__contains"] = oldDataPath

    # add extra arguments passed to the function.
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value

    response = call_api(params=params, api_type=obj_type)

    # filter out heavy fields
    if isinstance(response.get("results"), list):
        for entry in response["results"]:
            for field in STRIP_FIELDS:
                entry.pop(field, None)

    url_list = []
    for object in response["results"]:
        uuid_tmp = object["uuid"]
        url_tmp = f"https://catalogue.ceda.ac.uk/uuid/{uuid_tmp}/"
        confirmation = check_link(url_tmp)
        if confirmation == "responsive":
            url_list.append(url_tmp)
        else:
            url_list.append(f"Failed to create link for UUID: {uuid_tmp}")

    return {"response": response, "verified_urls": url_list}


# Possible things to search for (bbox might need Graham's suggestion)
"""
geographicExtent__bbox_Name??
geographicExtent__eastBoundLongitude
geographicExtent__westBoundLongitude
geographicExtent__southBoundLatitude
geographicExtent__northBoundLatitude

location__bboxName??
location__eastBoundLongitude
location__westBoundLongitude
location__southBoundLatitude
location__northBoundLatitude
"""
