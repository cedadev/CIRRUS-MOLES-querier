from common import call_api, API_TYPES

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
    page: int = 1,
    **kwargs
) -> dict:
    """
    placeholder function
    """
    obj_type = get_object_type(object_type)
    if not obj_type:
        return("Invalid object type. This must be any value from 'short_code' within your system prompt")
    
    params = {
        "page": page
    }
    
    if title:
        params["title__icontains"] = title
    if abstract:
        params["abstract__icontains"] = abstract
    if keywords:
        params["keywords__icontains"] = keywords
    
    if path:
        params["result_field__dataPath__startswith"] = path
        
    # add extra arguments passed to the function.
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value
    
    response = call_api(params=params, api_type=obj_type)
    
    return response["count"]


print(search_catalogue("ob", path="/neodc/sister"))

#make the path correct
#make sure they use icontains
# if doing an or, it may be required to merge dictionaries manually.
#add other proper fields rather than kwargs (maybe)
# make the logic nicer looking


# create list of links
# pagination is it showing the first 20 by default, but will say how many total there are. it is possible to go to a different page and see another 20
# remember to add the . for the common import


# Possible things to search for (bbox might need Graham's suggestion)
"""
creationDate
lastUpdatedDate
updateFrequency
dataLineage
publicationState
language
status
doiPublishedTime
geographicExtent__bbox_Name??
geographicExtent__eastBoundLongitude
geographicExtent__westBoundLongitude
geographicExtent__southBoundLatitude
geographicExtent__northBoundLatitude
result_field__oldDataPath
timePeriod__startTime
timePeriod_endTime

instrumentType

platformType
location__bboxName??
location__eastBoundLongitude
location__westBoundLongitude
location__southBoundLatitude
location__northBoundLatitude
"""
