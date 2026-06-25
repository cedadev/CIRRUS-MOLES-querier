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
    path: str = None, # OBSERVATION
    creationDate: str = None, # OBSERVATION
    lastUpdatedDate: str = None, # OBSERVATION
    updateFrequency: str = None, # OBSERVATION
    dataLineage: str = None, # OBSERVATION
    publicationState: str = None, # OBSERVATION + project + coll
    status: str = None, # OBSERVATION + project
    dataPublishedTime: str = None, # OBSERVATION + coll
    doiPublishedTime: str = None, # OBSERVATION + coll
    instrumentType: str = None, # instrument only
    platformType: str = None, # platform only
    timePeriodStart: str = None, # OBSERVATION
    timePeriodEnd: str = None, # OBSERVATION
    oldDataPath: list = None, # OBSERVATION
    page: int = 1,
    **kwargs,
) -> dict:
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
        "dataPublishedTime": dataPublishedTime,
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
    if "error" in response:
        return f"API Error fetching information: {response}"

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
