from mstranslator import Translator, ArgumentOutOfRangeException as outofrange
from bs4 import BeautifulSoup
from lxml import etree
import csv  # library for outputting csv files
import lxml.html
import os
import time
import numpy as np



class Co:
    """Short for COmpany, this class will contain all the data we need on each company"""
    def __init__(self, name = None, website = None):
        self.name = name
        self.reference = None # Is set to the reference comany if one is provided (See)
        if website[0:4] != 'http' and website[0:3] != 'See':
            #appends http heading if not already present and
            #checks if the provider is a subordinate of another provider
    	       website = 'http://' + website
        elif website[0:3] == 'See':
            self.reference = website[4:] #Reference to other Co to be implemented
        elif website[0:5] == 'Bought':
            self.reference = website[9:] #saw one case of "Bought by [some company]" in the excel file
        self.website = website
        self.content = [] # Contains a set of sublists of the form
                          # [dateAccessed, content]
        self.errors = []  # List of all errors encountered during attempts
                          # on this page


def findLanguage(co, translator):
    a = ''
    if co.content != []:
        try:
            html = lxml.html.fromstring(co.content[1])
            a = html.xpath('//html/@lang')
        except UnicodeDecodeError:  # some errors have occurred when decoding characters from non-English languages
            print("Unicode Decode Error with ", co.name)

        except etree.ParserError:
            print("ParserError with ", co.name)
        except etree.XMLSyntaxError:
            print("XMLSyntaxError with ", co.name)
        else:
            if a == []:
                soup = BeautifulSoup(co.content[1], "lxml")  # get html from site
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                text = text[:100]
                try:
                    a = translator.detect_lang(text)
                except TypeError:
                    a = 'type error'
            else:
                a = a[0]
    return a


def createCSVFile(fileName, rows):
    curr_dir = os.getcwd()
    savepath = os.path.join(curr_dir + "/data/" + fileName + time.strftime("%Y-%m-%d(%H_%M_%S)", time.gmtime()) + ".csv")
    with open(savepath, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(rows)

def listLang(coList, translator):
    language = []

    for co in coList:
        language.append((co.name, co.website, findLanguage(co, translator)))
    createCSVFile("Languages", language)

def npyImport(name = 'binaries.npy'):
    curr_dir = os.getcwd() #gets the current directory
    return np.load(curr_dir + os.sep + 'data' + os.sep + name)


translator = Translator('40b49a7a195e4a05a7bbe800342e073d')
coList = npyImport("01_01_2017.npy")
listLang(coList, translator)
