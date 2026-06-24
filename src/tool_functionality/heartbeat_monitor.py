import requests


def check_services():
    api = "https://api.catalogue.ceda.ac.uk/api/v3/"
    try:
        response = requests.get(api, timeout=5)
        # check codes are 200-399 range
        api_online = response.status_code < 400
    except requests.exceptions.RequestException:

        api_online = False

    # Check if Ollama is running
    ollama_url = "http://localhost:11434"
    try:
        ollama_response = requests.get(ollama_url, timeout=2)
        ollama_online = ollama_response.status_code == 200
    except requests.exceptions.RequestException:
        ollama_online = False

    return {"api_online": api_online, "ollama_online": ollama_online}
