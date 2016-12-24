# import urllib.error
# import urllib.request
# try:
#     urllib.request.urlopen('http://www.google.com')
# except urllib.error.HTTPError as e:
#     print(e.code)
# except urllib.error.URLError as e:
#     print(e.args)


# from urllib.request import urlopen
# a=urllib.urlopen('http://www.google.com/asdfsf')
# code = a.getcode()
# print(code)



# import requests

# response = requests.get('http://google.com')
# assert response.status_code < 400

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import openpyxl
import csv



spreadsheet = openpyxl.load_workbook('2015 CloudShare - December Final.xlsx')
data = spreadsheet.get_sheet_by_name('Data')

websites = []
for i in range(2, data.max_row):
	webpage = data.cell(row = i, column = 3).value
	if webpage[0:4] != 'http':
		webpage = 'http://' + webpage
	websites.append(webpage)


# text = open("Errors.txt", "w")
# text.write("Provider/Error\n")
textArray = []

for i in range(len(websites)):
	req = Request(websites[i])
	try:
		# code = urlopen(websites[i]).getcode()
		# if code == 200:
		# 	print('Website is working.')
		# else:
		# 	print('Working but not working')

	    response = urlopen(req)
	except ConnectionResetError:
		print('Server didn\'t send data')
		# ("{0} {1} {2}\n".format(i, data.cell(row = i + 2, column = 2).value , '/Server didn\'t send data'))
		textArray.append((i + 2, data.cell(row = i + 2, column = 2).value , 'Server didn\'t send data'))
	except HTTPError as e:
	    print('The server couldn\'t fulfill the request.')
	    # text.write("{0} {1} {2} {3}\n".format(i, data.cell(row = i + 2, column = 2).value, '/Error code: ', e.code))
	    textArray.append((i + 2, data.cell(row = i + 2, column = 2).value, 'HTTPError', e.code))
	    print(data.cell(row = i + 2, column = 2).value)
	    print('Error code: ', e.code)
	except URLError as e:
	    print('We failed to reach a server.')
	    # text.write("{0} {1} {2} {3}\n".format(i, data.cell(row = i + 2, column = 2).value, '/Reason: ', repr(e.reason)))
	    textArray.append((i + 2, data.cell(row = i + 2, column = 2).value, 'URLError ', repr(e.reason)))
	    print(data.cell(row = i + 2, column = 2).value)
	    print('Reason: ', e.reason)
	else:
	    print ('Website is working fine')


with open("test.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(textArray)
