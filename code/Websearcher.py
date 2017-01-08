import csv
import os
from urllib.request import Request, urlopen #Modules used to access websites with their URLs
from urllib.error import URLError, HTTPError #Modules used to deal with errors with accessing websites
from http.client import IncompleteRead #Strange error catch
from ssl import CertificateError #Strange error catch and bypass
import pprint
from bs4 import BeautifulSoup

from time import strftime, gmtime
from googleapiclient.discovery import build


my_api_key = "AIzaSyAbzWZuiWfXtI2tut_t0kc5xK6N1b2QnDM"
my_cse_id = "005958816095987214880:2wzfznrf0bw"

def GoogleSearchToList(num_results, start_index, search_term, excludedTerms):
    def google_search(search_term, api_key, cse_id, start_index, num_results, excludedTerms, **kwargs):
        # search_term (string): what are you searcing for
        # api_key (string): api_key of api
        # cse_id (string):
        items = []
        num_calls = (num_results // 10) + 1
        service = build("customsearch", "v1", developerKey=api_key)
        while num_calls > 0:
            if num_calls == 1:
                numberofresults = num_results - ((num_results // 10) * 10)
                if numberofresults == 0:
                    break
            else:
                numberofresults = 10
            res = service.cse().list(q=search_term, cx=cse_id, num=numberofresults, start=start_index,
                                     excludeTerms=excludedTerms, **kwargs).execute()
            num_calls -= 1
            start_index += 10
            items.extend(res['items'])
        return items

    results = google_search(search_term, my_api_key, my_cse_id, start_index, num_results, excludedTerms)
    URLs = []
    for result in results:
        URLs.append(result["formattedUrl"])
        print(result["formattedUrl"])
    return URLs


def SearchYandex(username, key, search_term, pages):
    urllist = []
    for page in range(pages):
        searchsite = "https://yandex.com/search/xml?" \
              "user=" + username + \
              "&key=" + key + \
              "&query=" + search_term + \
              "&l10n=en" \
              "&sortby=tm.order%3Dascending" \
              "&filter=none" \
              "&maxpassages=1" \
              "&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1" \
              "&page=" + str(page)

        req = urlopen(Request(searchsite)).read()
        soup = BeautifulSoup(req, "html.parser")
        for tag in soup.find_all("domain"):
            print(tag.text)
            urllist.append(tag.text)
    return urllist