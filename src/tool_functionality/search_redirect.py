from .common import check_link
from urllib.parse import quote_plus

def search_redirect(query: str) -> str:
    if query is None:
        return("Query must not be a None type")
    redirect_link = "https://cse.google.com/cse?cx=009617667314646343139:y6z_ljohx30#gsc.tab=0&gsc.q=" + quote_plus(query)
    confirmation = check_link(redirect_link)
    
    if confirmation == "responsive":
        return (redirect_link)
    else:
        return(f"Search Redirect Tool failed to create a valid link. This may be because the search is offline. The user can try to search the link and see if it works. link: {redirect_link}")

