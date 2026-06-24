from .common import call_api, API_TYPES


def get_record(UUID: str = None, URL: str = None) -> dict:
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

    # Extract UUID
    if UUID is None and URL:
        try:
            UUID = URL.split("/uuid/", 1)[1].split("/", 1)[0]
        except IndexError:
            return "You must enter a valid URL or UUID"
    if UUID is None and URL is None:
        return "You must enter a valid URL or UUID"

    # get uuid type
    type_params = {"fields": "short_code", "uuid": UUID}
    response = call_api(type_params, "referenceables")
    if "error" in response:
        return f"An error occurred While trying to get the short code of UUID {UUID}. This may mean the UUID does not exist. Error: {response}"

    try:
        short_code = response["results"][0]["short_code"]
    except IndexError:
        return f"Failed to get short code of UUID {UUID}. This may mean the UUID does not exist."

    if short_code not in API_TYPES:
        return f"Unknown API short code: {short_code}"
    endpoint = API_TYPES[short_code]

    information = call_api({"uuid": UUID}, endpoint)
    if "error" in information:
        return f"API Error fetching information: {information}"
    result = {}
    if information["results"] == []:
        return f"Failed to get data for UUID {UUID}. Reaching this far means the UUID exists within referencables and that was called successfully, so this is highly irregular (perhaps the API shut down between calls?)"

    for k, v in information["results"][0].items():
        if v not in ("", None, []):
            result[k] = v

    return result
