
from googleapiclient.discovery import build

my_api_key = "AIzaSyAbzWZuiWfXtI2tut_t0kc5xK6N1b2QnDM"
my_cse_id = "005958816095987214880:2wzfznrf0bw"

def google_search(search_term, api_key, cse_id, num_results, **kwargs):
    items = []
    num_calls = (num_results // 10) + 1
    service = build("customsearch", "v1", developerKey=api_key)
    start_index = 1
    while num_calls > 0:
        if num_calls == 1:
            numberofresults = num_results - ((num_results//10) *10)
            if numberofresults == 0:
                break
        else:
            numberofresults = 10
        res = service.cse().list(q=search_term, cx=cse_id, num = numberofresults, start = start_index, **kwargs).execute()
        num_calls -= 1
        start_index += 10
        items.extend(res['items'])
    return items

#main
results = google_search('data', my_api_key, my_cse_id, 10)
for result in results:
    print(result["formattedUrl"])
