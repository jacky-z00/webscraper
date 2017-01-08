import numpy as np
from urllib.request import Request, urlopen #Modules used to access websites with their URLs
from urllib.error import URLError, HTTPError #Modules used to deal with errors with accessing websites
from http.client import IncompleteRead #Strange error catch
from ssl import CertificateError #Strange error catch and bypass
import ssl
import csv
import time
import os

# imports a npy file from a specified path
def npyImportPathSpecific(path, name = 'binaries.npy'):
    return np.load(path + name)


# input url and return HTMLelement containing data of website
def loadURL(url):
    if url[0:4] != 'http':
        url = 'http://' + url
    context = ssl._create_unverified_context()  # bypasses SSL Certificate Verfication (proabably not a good idea, but it got more sites to work)
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'})  # changing the header prevents some webscraper blocking techniques
    try:

        response = urlopen(req, context=context).read()  # opens the URL and returns data (in bytes)
    except ConnectionResetError:
        print('Server didn\'t send data' + ' ' + url)
        return
    except HTTPError as e:
        print('HTTPError: ' + str(e.code) + ' ' + url)
        return
    except URLError as e:
        print('We failed to reach a server. ' + url)
        return
    except CertificateError:
        print("SSL Certificate Error with ", url)
        return
    except IncompleteRead as e:
        print("IncompleteRead Error with ", url)
        return
    return response


# checks if URL works, returns True if it does and False if it doesn't
def UrlCheck(url):
    if url[0:4] != 'http':
        url = 'http://' + url
    try:
        context = ssl._create_unverified_context()  # bypasses SSL Certificate Verfication (proabably not a good idea, but it got more sites to work)
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'})  # changing the header prevents some webscraper blocking techniques

        urlopen(req, context=context)  # opens the URL and returns data (in bytes)
    except ConnectionResetError:
        return False
    except HTTPError as e:
        return False
    except URLError as e:
        return False
    except CertificateError:
        return False
    except IncompleteRead as e:
        return False
    else:
        return True


# write a single row into a given csvfile (path needs to be included in parameter)
def writeIntoCSV(csvfile, row):
    with open(csvfile, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


# from a CSV file, compile the elements from one column into a list (in this case, a list of URLs, but other things can work too)
def getUrlsFromCSV(csvfile):
    UrlList = []
    with open(csvfile) as f:
        list = [line.split() for line in f]  # create a list of lists
        for x in list:  # print the list items
            UrlList.append(x[1])
    f.close()
    return UrlList


# create a CSV file with the given savepath, filename and rows (in array form) info
def createCSVFile(savepath, filename, rows):

    # adds date and time to end of file name to avoid overwriting
    savepath = os.path.join(savepath + filename + time.strftime("%Y-%m-%d(%H_%M_%S)", time.gmtime()) + ".csv")

    with open(savepath, "w", encoding = 'utf-8') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(rows)
