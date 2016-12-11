import csv

from bs4 import BeautifulSoup
import requests
import urllib
import numpy as np
import pandas as pd
from datetime import datetime
import time

############################
# prepare stick index data #
############################

##process DJIA: append tag to indicate a rise in stock index:'+' and a drop in stock index:'-'
count = 0
DJIA = []
with open("DJIA.csv") as f:
	reader = csv.reader(f,delimiter=',')
	for row in reader:
		if(count!=0):
			DJIA.append(row)
		count = count+1

DJIA = DJIA[::-1]
for i in range(0,len(DJIA)):
	if(i!=0):
		if(DJIA[i][4]>=DJIA[i-1][4]):
			DJIA[i].append("+")
		elif(DJIA[i][4]<DJIA[i-1][4]):
			DJIA[i].append("-")

with open('DJIA_trend.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for row in DJIA:
        thedatawriter.writerow(row)

##process NASDQUE: append tag to indicate a rise in stock index:'+' and a drop in stock index:'-'
count = 0
NASDQUE = []
with open("NASDQUE.csv") as f:
	reader = csv.reader(f,delimiter=',')
	for row in reader:
		if(count!=0):
			NASDQUE.append(row)
		count = count+1

NASDQUE = NASDQUE[::-1]
for i in range(0,len(NASDQUE)):
	if(i!=0):
		if(NASDQUE[i][4]>=NASDQUE[i-1][4]):
			NASDQUE[i].append("+")
		elif(NASDQUE[i][4]<NASDQUE[i-1][4]):
			NASDQUE[i].append("-")


with open('NASDQUE_trend.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for row in NASDQUE:
        thedatawriter.writerow(row)

##########################################
# prepare news headline data from Reddit #
##########################################
def parse_page(url):
    html = requests.get(url).content
    page = BeautifulSoup(html,"html.parser")
    contents = page.find_all("div")
    news = {}

    for content in contents:
        header = content.find(class_="search-title may-blank")
        if (header is not None):
            header = header.get_text()        
        
        score = content.find(class_="search-score")
        if (score is not None):
            score = score.get_text()
            
        new_date = content.find("time")
        if (new_date is not None):
            new_date = new_date["datetime"][:10]
            
        if (header is not None):
            news[header] = new_date
            
    return news

dates = pd.date_range('10/03/2011', periods=1834, freq='D')
index = pd.DatetimeIndex(dates)
new_index = list(index.astype(np.int64) // 10 ** 9)
prefix = "https://www.reddit.com/r/worldnews/search?q=timestamp%3A"
postfix = "&restrict_sr=on&sort=top&t=all&syntax=cloudsearch"
url = []
for i in range(len(new_index) - 1):
    url.append(prefix + str(new_index[i]) + ".." + str(new_index[i + 1]) + postfix)

for link in url:
    news=""
    while(len(news)==0):
        news = parse_page(link)
        time.sleep(3) 
    for new in news:
        new_list = [news[new],new]
        with open('news_headline.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(new_list)
writer.close()