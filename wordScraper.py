from bs4 import BeautifulSoup
import collections
from http.client import IncompleteRead, BadStatusLine
import ssl
import urllib.request 
import re


def word_index(site):
    
    # Words we don't care about
    useless_words = ['the', 'contact', 'us', 'and', 'subscribe', 'our', 'visit', 'all', 'rights', 'reserved',
                'your', 'for', 'more', 'read', 'their', 'with', 'every', 'you', 'what', 'why', 'how', 'new', 'are', 'that', 'from'
                    'get', 'can' 'see', 'use', 'about', 'have' 'this','now', 'has', 'will', 'not', 'its']  
    
    #fix certain links
    def http_to_site(site):
        if site[:4] != 'http':
            site = 'http://' + site
        return site
    site = http_to_site(site)
    # Header to bypass firewalls
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

    req = urllib.request.Request(site, headers=hdr) # adds headers to request website

    context = ssl._create_unverified_context() # allow access of unverified certificate websites
    
    try:
         page = urlopen(req, context = context) # opens site
    except ConnectionResetError:
         return collections.Counter()
    except urllib.error.URLError as e:
        return collections.Counter()
    except HTTPError as e:
        return collections.Counter()
    except http.client.IncompleteRead as e:
        return collections.Counter()
    except http.client.BadStatusLine:
        return collections.Counter()
    except ssl.CertificateError:
        return collections.Counter()
    
    # ignore words shorter than 3 letters, numbers, and words in useless_words
    def validate_word(word):
        if len(word) > 2 and not word[0].isdigit() and word not in useless_words:
            return word

# Function to scrape text
    def text_scraper(site):
        
        soup = BeautifulSoup(page,"lxml") # get html from site

    # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

    # get text
        text = soup.get_text()

    # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

    words_index =  re.findall(r'\w+', text_scraper(site).lower()) # find only words and make them lower case
    
    word_in_text = [validate_word(word) for word in words_index if validate_word(word) is not None]
    
    word_indexing = collections.Counter() # add each word to counter
    
    for word in word_in_text:
        word_indexing[word] += 1
        
    return collections.Counter(word_in_text)


def word_scrape_list_of_sites(list_of_sites):
    list_index = [word_index(site) for site in list_of_sites]
    return list_index

def combine_counters(list_of_counters):
    total_index = collections.Counter()
    for counter in list_of_counters:
        total_index.update(counter)
    return total_index
