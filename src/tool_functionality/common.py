import requests

OBSERVATION_API_URL = "http://api.catalogue.ceda.ac.uk/api/v3/"
DEFAULT_PAGE_SIZE = 10


def call_api(params: dict, api_type: str, page: int = 1) -> dict:
    """
    Call the CEDA observations API with the given parameters.
    Applies pagination and returns the JSON response as a Python dict.
    """
    paginated_params = {
        **params,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (page - 1) * DEFAULT_PAGE_SIZE,
    }

    try:
        response = requests.get(
            OBSERVATION_API_URL + api_type,
            params=paginated_params,
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {e}",
            "params": paginated_params,
        }
    except ValueError as e:
        return {
            "error": f"Failed to parse JSON: {e}",
            "params": paginated_params,
        }

    return data


def check_link(url):
    try:
        r = requests.get(url, timeout=15)
        if 200 <= r.status_code < 300:
            return "responsive"
        return "out_of_range"
    except Exception:
        return "unresponsive"


API_TYPES = {
    "ob": "observations",
    "comp": "computations",
    "instr": "instruments",
    "proj": "projects",
    "plat": "platforms",
    "coll": "observationcollections",
}
