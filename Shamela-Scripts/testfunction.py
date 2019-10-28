from bs4 import BeautifulSoup
import csv, os, json



page_html = BeautifulSoup(open(r'/mnt/c/Users/smerchant/151045'),'html.parser')
content = page_html.find_all('span', attrs={'class':'info-item'})

d = {}
keyList = ['Book', 'Author', 'Publisher','Edition','Pages', 'Views','Date Added']

for row in content:
    
    #coll[0].append(row.find('span',attrs={'class':'info-title'}).text)
    #coll[1].append(row.find('span', attrs={'class':'info-desc'}).text)
    d[row.find('span',attrs={'class':'info-title'}).text] = row.find('span', attrs={'class':'info-desc'}).text

print(d)
