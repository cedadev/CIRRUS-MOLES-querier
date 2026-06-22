import requests

def check_link(url):
    try:
        r = requests.get(url, timeout=15)
        if 200 <= r.status_code < 300:
            return "responsive"
        return "out_of_range"
    except Exception:
        return "unresponsive"