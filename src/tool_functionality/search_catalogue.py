from .common import call_api, check_link, API_TYPES
import re

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


def check_year(value):
    return bool(re.match(r"^\d{4}$", str(value)))


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
    dataPublishedTime: str = None,
    doiPublishedTime: str = None,
    instrumentType: str = None,
    platformType: str = None,
    timePeriodStart: str = None,
    timePeriodEnd: str = None,
    page: int = 1,
    **kwargs,
) -> dict:
    obj_type = get_object_type(object_type)
    if not obj_type:
        return "Invalid object type. This must be any value from 'short_code' within your system prompt"

    params = {}

    icontains_fields = {
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "updateFrequency": updateFrequency,
        "dataLineage": dataLineage,
        "publicationState": publicationState,
        "status": status,
        "instrumentType": instrumentType,
        "platformType": platformType,
    }

    # Add icontains if there are values
    for api_param, value in icontains_fields.items():
        if value:
            params[f"{api_param}__icontains"] = value
    
    
    range_fields = {
        "dataPublishedTime": dataPublishedTime,
        "doiPublishedTime": doiPublishedTime,
        "lastUpdatedDate": lastUpdatedDate,
    }
    
    # Add range if there are values and they are years
    for api_param, value in range_fields.items():
        if value and check_year(value):
            params[f"{api_param}__gte"] = f"{value}-01-01"
            params[f"{api_param}__lte"] = f"{value}-12-31"
    
    

    # nested filters
    if path:
        params["result_field__dataPath__startswith"] = path
    if creationDate: # TODO test
        if check_year(creationDate):
            params["creationDate__year"] = creationDate
        else:
            return(f"creationDate not a year. You put: {creationDate}")
    if timePeriodStart: # TODO test
        if check_year(timePeriodStart):
            params["timePeriod__startTime__gte"] = f"{timePeriodStart}-01-01"
            params["timePeriod__startTime__lte"] = f"{timePeriodStart}-12-31"
        else:
            return(f"timePeriodStart not a year. You put: {timePeriodStart}")
    if timePeriodEnd: # TODO test
        if check_year(timePeriodEnd):
            params["timePeriod__endTime__gte"] = f"{timePeriodEnd}-01-01"
            params["timePeriod__endTime__lte"] = f"{timePeriodEnd}-12-31"
        else:
            return(f"timePeriodEnd not a year. You put: {timePeriodEnd}")

    # add extra arguments passed to the function.
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value

    response = call_api(params=params, api_type=obj_type, page=page)
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
