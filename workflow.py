# -*- coding: utf-8 -*-
"""
Created on Dec 27 2016
"""
#This file will contain the developing workflow of the whole project
# as an updating combination of functionality developed elsewhere


import openpyxl #library for pulling data from excel files
import csv #library for outputting csv files
import ssl #deals with SSL Certificate Errors
import os
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen #Modules used to access websites with their URLs
from urllib.error import URLError, HTTPError #Modules used to deal with errors with accessing websites
from http.client import IncompleteRead #Strange error catch
from ssl import CertificateError #Strange error catch and bypass
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import collections


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
        self.website = website
        self.content = [] # Contains a set of sublists of the form
                          # [dateAccessed, content]
        self.errors = []  # List of all errors encountered during attempts
                          # on this page

"""imports a correctly formatted spreadhseet as a list of Co objects"""
def excelToCo(inpath = '2015 CloudShare - December Final.xlsx', outpath = None):
    coList = []
    curr_dir = os.getcwd() #gets the current directory
    spreadsheet = openpyxl.load_workbook(curr_dir + os.sep + 'data' + os.sep + inpath) #pulls data directly from excel file
    data = spreadsheet.get_sheet_by_name('Data') #specifies which sheet to pull data from

    for i in range(2, data.max_row):
        coList.append(Co(data.cell(row = i, column = 2).value,
                         data.cell(row = i, column = 3).value))
    np.save(curr_dir + os.sep + 'data' + os.sep + (outpath if outpath else time.strftime("%d_%m_%Y")), coList)
    return coList

"""takes a list of Co objects and attempts to fill out their website content,
   errors encounters, and dates of access using basic html methods
   Ignores duplicates/references"""
def coUpdateHTML(colist, lim = -1, outpath = None):
    colist = colist[0:lim]
    for co in colist: #iterates through every Co object

    	if (co.reference == None): #ensures not a reference
    		context = ssl._create_unverified_context() #bypasses SSL Certificate Verfication (proabably not a good idea, but it got more sites to work)
    		req = Request(co.website, headers = {'User-Agent': 'Mozilla/5.0'}) #changing the header to Mozilla/5.0 prevents some webscraper blocking techniques
    		try:

    		    response = urlopen(req, context = context).read() #opens the URL and returns data (in bytes)


    #Various errors have popped up, so I set up exceptions to catch them. Should be a better way to do this.
    		except ConnectionResetError:
    			print('Server didn\'t send data')
    			co.errors.append(co.name + ' Server didn\'t send data'+ ' '+ co.website)
    		except HTTPError as e:
    		    print('The server couldn\'t fulfill the request.')
    		    co.errors.append(co.name + ' HTTPError: '+ str(e.code) + ' '+ co.website)
    		    print(co.name)
    		    print('Error code: ', e.code)
    		except URLError as e:
    		    print('We failed to reach a server.')
    		    co.errors.append(co.name + ' URLError ' + repr(e.reason) + ' '+ co.website)
    		    print(co.name)
    		    print('Reason: ', repr(e.reason))
    		except CertificateError:
    			print("SSL Certificate Error")
    			co.errors.append(co.name + ' SSL Certificate Error'+ ' ' + co.website)
    			print(co.name)
    		except IncompleteRead as e:
    			print("IncompleteRead Error")
    			co.errors.append(co.name + ' Incomplete Read Error' + ' ' + co.website)
    			print(co.name)

    		else: #if no web based error occurs
    			try:
    				saveWebPage = response.decode() #data (in bytes) from opening URL is decoded into String format
    			except UnicodeDecodeError: #some errors have occurred when decoding characters from non-English languages
    				print("Unicode Decode Error")
    				co.errors.append(co.name +  ' Decode Error' + ' ' + co.website)
    			else:

    				"""Store the website content"""
    				co.content = [time.strftime("%d/%m/%Y"), saveWebPage]
    				print (co.name + ' is working fine')
    curr_dir = os.getcwd() #gets the current directory
    np.save(curr_dir + os.sep + 'data' + os.sep + (outpath if outpath else time.strftime("%d_%m_%Y")), colist)
                                            #Updates the saved binaries
                                            #if no name is provided it uses the date
    return colist
"""takes a list of Co objects and attempts to fill out the website content,
   of the cos that encountered errors before using selenium web driver
   Ignores duplicates/references"""
def coUpdateSelenium(colist, lim = -1, outpath = None):
    count = 0
    colist = colist[0:lim]
    driver = webdriver.Firefox()
    for co in colist: #iterates through every Co object that errored
        if co.errors != []:

            driver.get(co.website)
            if driver.page_source:
                count = count + 1
                co.content = [time.strftime("%d/%m/%Y"), driver.page_source]
                print (co.name + ' is working fine with selenium')
            else:
                print ("Selenium issue")
                co.errors.append("Selenium issue")

    driver.close()
    print(str(count))
    curr_dir = os.getcwd() #gets the current directory
    np.save(curr_dir + os.sep + 'data' + os.sep + (outpath if outpath else time.strftime("%d_%m_%Y")), colist)
                                            #Updates the saved binaries
                                            #if no name is provided it uses the date
    return colist

def word_index(colist):

    # Words we don't care about
    useless_words = ['the', 'contact', 'us', 'and', 'subscribe', 'to', 'on', 'a', 'our', 'visit', 'all', 'rights', 'reserved',
                'your', 'for', 'more', 'read', 'their', 'with', 'every', 'you', 'what', 'why', 'how', 'new']

    # ignore words shorter than 3 letters, numbers, and words in useless_words
    def validate_word(word):
        if len(word) > 2 and not word[0].isdigit() and word not in useless_words:
            return word

# Function to scrape text
    def text_scraper(site):

        soup = BeautifulSoup(site,"html.parser") # get html from site

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

    word_indexing = collections.Counter() # add each word to counter
    for co in colist:
        if co.content != []:

            words_index = re.findall(r'\w+', text_scraper(co.content[1]).lower()) # find only words and make them lower case

            word_in_text = [validate_word(word) for word in words_index if validate_word(word) is not None]



            for word in word_in_text:
                word_indexing[word] += 1

    word_indexing = [[i, word_indexing[i]] for i in word_indexing if word_indexing[i] > 10]
    return word_indexing
    #collections.Counter(word_in_text)



def npyImport(name = 'binaries.npy'):
    curr_dir = os.getcwd() #gets the current directory
    return np.load(curr_dir + os.sep + 'data' + os.sep + name)



"""Here is the main workflow"""
#r = excelToCo()
#r = coUpdateHTML(r, lim = 5)






