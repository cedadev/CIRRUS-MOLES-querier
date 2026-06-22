import requests
from enum import Enum

OBSERVATION_API_URL = "http://api.catalogue.ceda.ac.uk/api/v3/"


def call_api(params: dict, api_type: str) -> dict:
    """
    Call the CEDA observations API with the given parameters.
    Applies pagination and removes heavy fields from each dataset.
    Returns the JSON response as a Python dict.
    """

    try:
        response = requests.get(
            OBSERVATION_API_URL+api_type,
            params=params,
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {e}",
            "params": params,
        }
    except ValueError as e:
        return {
            "error": f"Failed to parse JSON: {e}",
            "params": params,
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
    "coll": "observationcollections"
}