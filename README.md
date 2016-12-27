# webscraper

**************DEPENDENCIES**************
---------------------------------
doxygen|pandas|urllib.request|urllib.parse|openpyxl|csv|ssl|os|time|selenium

**************INSTRUCTIONS FOR USE**************
---------------------------------
Each of the functions in workflow save binary arrays as .npy files. Running any of them
will return a list of Co objects, but will also save a binary to the data folder.
If you want to access a binary in the data folder, use the npyImport(name='') function
and add the name of the npy file in data you're interested in.
excelToCo() imports from an excel
coUpdateHTML() takes a list of Cos and updates them with HTML scraping
coUpdateSelenium() takes a list of Cos and updates the error-ones with Selenium scraping
**************BASIC STEPS**************
---------------------------------
Decide on and set up an environment to work in, possibly flask, that we are all comfortable with

Divy up parts of the project based on skill, Projects 1 and 2 can be done separately
Discuss CSV/SQL data format

Project 1)
---------------------------------
A program that is able to run through the Cloudshare excel and
Validate the company still exists, is a real company
Validate that there is activity on the site – meaning that something changed over a 3-week period.  No change, that means that the company is probably not in business anymore – then try checking again at the 6 week level, using the crawler.
This would have to be a server hosted application that ran automatically every day/week and tracked changes in the web-pages it visited to flag inactive websites.

Project 2) /here by Feb 1/
---------------------------------
Run through the Cloudshare websites and compile a list of keywords/phrases/website characteristics
Vet those search terms for usefulness

Project 3)
---------------------------------
Select a search engine API (probably google but who knows) that we can integrate into our code
Use the honed search terms from project 2 to search the web for new company sites
Verify manually that companies are actually being identified by the crawler and get creative trying to figure out how to improve the algorithm, learning some machine learning libraries, etc.
The precision of our model matters more than the accuracy here, we could submit this and be done

Project 4) /here by April 1/
---------------------------------
Create a GUI to visualize our results in for people less well acquainted with computer science
Provide support, potentially get active feedback from people high in the IDC infrastructure for changes and additions
If they like the result we have, it is likely they will want us to fine tune it for further compensation


**************PATH FORWARD**************
---------------------------------
1) Create a script that is just a series of functions in python to do:
---------------------------------
    A) Create classes that we're gonna use to store our data in a python file
    B) Import the excel into binaries
    C) Create a python file that has functions to scrape and return websites
2)
---------------------------------



