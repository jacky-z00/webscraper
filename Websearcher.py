
from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyAbzWZuiWfXtI2tut_t0kc5xK6N1b2QnDM"
my_cse_id = "005958816095987214880:2wzfznrf0bw"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
    'stackoverflow site:google.com', my_api_key, my_cse_id, num=10)
for result in results:
    pprint.pprint(result)