from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv, os, json

url = 'http://shamela.ws/index.php/search/last/'
base_url = 'http://shamela.ws'
with open('shameladetails.csv', 'w', encoding="utf-8") as f:
    header = ['bookTitle', 'bookUrl', 'bok_file_Url']
    writer = csv.DictWriter(f, fieldnames=header, delimiter=",")
    writer.writeheader()

    # There was 77 pages 
    for p in range(1,77):
        raw_html = get(url+'page-'+str(p))
        html = BeautifulSoup(raw_html.content, 'html.parser')
        booksCollections = []
        bok_file_Url = []
        indexContainer = html.find('table')
        rows = indexContainer.find_all('tr')
    
        for row in rows:
            for cols in row.find_all('td', attrs={'class': 'regular-book'}):
            
                book = {}
                bookUrls = cols.find('a').get_attribute_list('href')[0]
                bookTitles = cols.find('a').text
                #print(bookTitles)
                book['bookTitle']= bookTitles
                book['bookUrl']= base_url+bookUrls
                booksCollections.append(book)
                #print(book)

        for item in booksCollections:
            #print(item['bookUrl'])
            page_row_file = get(item['bookUrl'])
            page_html = BeautifulSoup(page_row_file.content, 'html.parser')
            
            #Since there was no div class or style.  The bok image was targeted
            tags = page_html.find_all('img', {'src':'/files/img/front/bok.png'})
            for previous_tag in tags:
                link = previous_tag.findPrevious('a').get_attribute_list('href')[0]
                item['bok_file_Url'] = link
                #print(base_url+link)
            writer.writerow(item)
       #print(booksCollections)
        # for a in booksCollections:
        #     print(a)


## not in used           
def get_book_metadata(page_url):
     page_row_file = get(page_url)
     page_html = BeautifulSoup(page_row_file.content, 'html.parser')
     content = page_html.find_all('span', attrs={'class':'info-item'})
    
    book = {}
    for row in content:
        book['title'] = row.find('span',attrs={'class':'info-title'}).text
        book['desc'] = row.find('span', attrs={'class':'info-desc'}).text
        print(book)





