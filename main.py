#import dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words

#get data from Wikipedia
wikipedia_api_link="https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki"

if (len(sys.argv) < 2 ):
    print ('Enter valid string')
    exit()

#get the search word
string_query = sys.argv[1]

if(len(sys.argv) > 2):
    search_mode=True
else:
    search_mode = False

#create our URL
url = wikipedia_api_link + string_query

try:
    response = requests.get(url)
    data = json.loads(response.content.decode('utf-8'))

    #format this data
    wikipedia_page_tag = data['query']['search'][0]['title']

    #create our new url
    url = wikipedia_link + wikipedia_page_tag
    page_word_list = getWordList(url)
    #create table of word counts
    page_word_count = createFrequencyTable(page_word_list)
    sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
    #remove stop words
    if (search_mode):
        sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    #sum total words to calculate the frequencies
    total_words_sum = 0
    for key, value in sorted_word_frequency_list:
      total_words_sum = total_words_sum + value

    #just get the top 20 words
    if len(sorted_word_frequency_list) > 20:
        sorted_word_frequency_list = sorted_word_frequency_list[:20]

    #create our final list, words frequency + percentage
    final_list = []
    for key, value in sorted_word_frequency_list:
        percentage_value = float(value * 100) / total_words_sum
        final_list.append(key, value, round(percentage_value, 4))

        print_headers = ['Word', 'Frequency', 'Frequency Percentage']



#parse and format data
#sort the data
#print the data
