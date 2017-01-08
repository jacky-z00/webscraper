import tldextract
import csv
from .workflow import Co
from .utils import createCSVFile
from .utils import npyImportPathSpecific, UrlCheck, writeIntoCSV, getUrlsFromCSV
from .langChecker import findLanguage
from urllib.request import Request, urlopen #Modules used to access websites with their URLs
from urllib.error import URLError, HTTPError #Modules used to deal with errors with accessing websites
from http.client import IncompleteRead #Strange error catch
from ssl import CertificateError #Strange error catch and bypass
import ssl



def getDomains(fromSource, returnType, urllist = None, coList = None, savepath = None, sourcefilename = None, sourcefilepath = None):
    domainsdict = {}
    if fromSource == "npy":
        coList = npyImportPathSpecific(sourcefilepath, sourcefilename)
        fromSource = "coList"

    if fromSource == "coList":
        for co in coList:
            parsed_url = tldextract.extract(co.website)
            domain = parsed_url[1]
            domainsdict[domain] = co.website

    if fromSource == "urllist":
        for url in urllist:
            domain = getDomain(url)
            domainsdict[domain] = url

    if fromSource == "csv":
        with open(sourcefilepath + sourcefilename) as f:
            mycsv = csv.reader(f)
            for row in mycsv:
                if len(row) > 1:
                    domainsdict[row[0]] = row[1]

    if returnType == "urldomaindict":
        return domainsdict
    if returnType == "csv":
        createCSVFile(savepath, "domains", list(domainsdict.items()))
    if returnType == "list":
        return domainsdict.keys()


def getDomain(url):
    try:
        parsed_url = tldextract.extract(url)
    except:
        return "TypeError"
    else:
        domain = parsed_url[1]
        return domain

def compareDomain(domain1, domain2):
    return domain1.lower() == domain2.lower()


def compareDomains(coList, newurllist, pathToFile, search_term, translator):
    existingdomains1 = getDomains("coList", "list", coList = coList)
    existingdomains2 = getDomains("csv", "list", sourcefilename="New_Websites.csv", sourcefilepath=pathToFile)
    existingdomains = list(existingdomains1) + list(existingdomains2)
    newdomainsdict = getDomains("urllist", "urldomaindict", urllist=newurllist)
    writeIntoCSV(pathToFile + "New_Websites.csv", "")
    for newdomain in list(newdomainsdict.keys()):
        url = newdomainsdict[newdomain]
        alreadyExists = False
        for existingdomain in existingdomains:
            if compareDomain(existingdomain, newdomain):
                alreadyExists = True
        if not alreadyExists and UrlCheck(url):
            language = findLanguage("url", url, translator)
            writeIntoCSV(pathToFile + "New_Websites.csv", (newdomain, url, search_term, language))

