

from urllib.request import Request, urlopen #Modules used to access websites with their URLs
from urllib.error import URLError, HTTPError #Modules used to deal with errors with accessing websites
from http.client import IncompleteRead #
from ssl import CertificateError #
import openpyxl #library for pulling data from excel files
import csv #library for outputting csv files
import ssl #deals with SSL Certificate Errors


# spreadsheet = openpyxl.load_workbook('Test.xlsx')
# data = spreadsheet.get_sheet_by_name('Sheet1')

spreadsheet = openpyxl.load_workbook('2015 CloudShare - December Final.xlsx') #pulls data directly from excel file
data = spreadsheet.get_sheet_by_name('Data') #specifies which sheet to pull data from



"""checks if a text contains a specified character"""
def checkForCharacter(character, text):
	for x in text:
		if x == character:
			return True
	return False

"""in a specified text, replaces all instances of a specified
	character with a new character"""
def replaceAll(characterToBeReplaced, newCharacter, text):
	text = list(text)
	for i in range(len(text)):
		if text[i] == characterToBeReplaced:
			text[i] = newCharacter
	return ''.join(text)


websites = [] #stores all the URLs
for i in range(2, data.max_row):
	webpage = data.cell(row = i, column = 3).value
	if webpage[0:4] != 'http' and webpage[0:3] != 'See': #appends http heading if not already present and checks if the provider is a subordinate of another provider
		webpage = 'http://' + webpage
	websites.append(webpage)




textArray = [] #stores all the websites that return an error (later written into a CSV file, each element is a row in the CSV file)
textArray.append(("Row", "Provider", "Error Message", "Error Code", "Website"))
for i in range(len(websites)): #iterates through every website

	if (websites[i][0:3] == 'See'): #checks for subordinate case first and ends current loop if true
		print("Duplicate")
		textArray.append((i + 2, data.cell(row = i + 2, column = 2).value , 'Duplicate', ' ', data.cell(row = i + 2, column = 3).value))
	else:

		context = ssl._create_unverified_context() #bypasses SSL Certificate Verfication (proabably not a good idea, but it got more sites to work)
		req = Request(websites[i], headers = {'User-Agent': 'Mozilla/5.0'}) #changing the header to Mozilla/5.0 prevents some webscraper blocking techniques
		try:
		
		    response = urlopen(req, context = context).read() #opens the URL and returns data (in bytes)


"""Various errors have popped up, so I set up exceptions to catch them. Should be a better way to do this."""
		except ConnectionResetError:
			print('Server didn\'t send data')
			textArray.append((i + 2, data.cell(row = i + 2, column = 2).value , 'Server didn\'t send data', ' ', data.cell(row = i + 2, column = 3).value))
		except HTTPError as e:
		    print('The server couldn\'t fulfill the request.')
		    textArray.append((i + 2, data.cell(row = i + 2, column = 2).value, 'HTTPError', e.code, data.cell(row = i + 2, column = 3).value))
		    print(data.cell(row = i + 2, column = 2).value)
		    print('Error code: ', e.code)
		except URLError as e:
		    print('We failed to reach a server.')
		    textArray.append((i + 2, data.cell(row = i + 2, column = 2).value, 'URLError ', repr(e.reason), data.cell(row = i + 2, column = 3).value))
		    print(data.cell(row = i + 2, column = 2).value)
		    print('Reason: ', e.reason)
		except CertificateError:
			print("SSL Certificate Error")
			textArray.append((i + 2, data.cell(row = i + 2, column = 2).value , 'SSL Certificate Error', ' ', data.cell(row = i + 2, column = 3).value))
			print(data.cell(row = i + 2, column = 2).value)
		except IncompleteRead as e:
			print("IncompleteRead Error")
			textArray.append((i + 2, data.cell(row = i + 2, column = 2).value , 'Incomplete Read Error', ' ', data.cell(row = i + 2, column = 3).value))
			print(data.cell(row = i + 2, column = 2).value)

		else: #if no error occurs
			try:
				saveWebPage = response.decode() #data (in bytes) from opening URL is decoded into String format
			except UnicodeDecodeError: #some errors have occurred when decoding characters from non-English languages
				print("Unicode Decode Error")
				textArray.append((i + 2, data.cell(row = i + 2, column = 2).value, 'Decode Error', ' ', data.cell(row = i + 2, column = 3).value))
			else:

				"""create a text file to store html file of the website"""
				fileName = data.cell(row = i +2, column = 2).value
				if checkForCharacter('/', fileName):
					fileName = replaceAll('/', '_', fileName)
				newFile = open(fileName + '.html', 'w')
				newFile.write(saveWebPage)
				newFile.close()
				print (data.cell(row = i + 2, column = 2).value, ' is working fine')


"""write all data in textArray into a CSV file"""
with open("test7.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(textArray)
