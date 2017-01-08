from webscraper import workflow, domains, Websearcher, utils
from mstranslator import Translator
import os


Co = workflow.Co
curr_dir = os.getcwd()

#Fill in these parameters for either search
savepath = os.path.join(curr_dir + "/webscraper/data/")
search_term = "cloud management data"
excludedTerms = None
translator = Translator('40b49a7a195e4a05a7bbe800342e073d')


coList = utils.npyImportPathSpecific(savepath, "03_01_2017.npy")

#Google Search
num_results = 10
start_index = 1
UrlList = Websearcher.GoogleSearchToList(num_results, start_index, search_term, excludedTerms)

# #Yandex Search
# num_pages = 10
# username = "jac-zhu"
# key = "03.453213766:7fb6a56551c3e48d99d27c1dc132677c"
# UrlList = Websearcher.SearchYandex(username, key, search_term, num_pages)

domains.compareDomains(coList, UrlList, savepath, search_term, translator) #append the new websites to existing New_Websites.csv file (which savepath should lead to)


