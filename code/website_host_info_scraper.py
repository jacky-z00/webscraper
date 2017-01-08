
# coding: utf-8

# In[ ]:

from bs4 import BeautifulSoup
import csv
import json
import requests
import socket
from urllib.request import urlopen
from urllib.parse import urlparse


working_websites = csv.reader(open('Working_Websites2016-12-30_10_05_07.csv'))
list_working_websites = []
for row in working_websites:
    list_working_websites.append(row[2])
list_working_websites = list_working_websites[1:]


#gathers host information of the website using freegeoip.net,
#a public HTTP API for software developers to search the geolocation of IP addresses.

def get_site_info(website):
    url_parsed = urlparse(website)
    host_name = url_parsed.hostname
    
    def get_ip(website):
        try:
            ip = socket.gethostbyname(host_name) #get ip address if possible
        except socket.gaierror:
            ip = "Unable to retreive IP address"
        return ip
    
    ip = get_ip(website)
    
    if ip == "Unable to retreiev IP address": 
        url =  "http://www.freegeoip.net/json/" + url_parsed.netloc #Use trimmed url if unable to use IP
    else:
        url = "http://www.freegeoip.net/json/" + ip #Use IP
    
    try:
        r = requests.get(url)
        web_info = r.json() #gathers the requested website information in a dictionary
        web_info["Website"] = website #add website name into the dictionary that contains information about the website
    except json.JSONDecodeError: 
        return {"Website": website} # returns only a dictionary of only the website if the url doesn't work
    
    return web_info

[get_site_info(website) for website in list_working_websites] # runs the scraper through the list of sites
keys = website_info[0].keys()

with open('website_host_info.csv', 'w', newline='',encoding='utf-8') as output_file: #export into csv
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(website_info)
    
#Note: Leading zeros (ie. 0xxxx) is not shown on csv when opened with excel and requires a bit of tinkering
#refer to http://www.upenn.edu/computing/da/bo/webi/qna/iv_csvLeadingZeros.html 

