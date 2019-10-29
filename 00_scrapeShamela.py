"""
Scrape all books from al-Maktaba al-Shamela:
Use the page where all the books are listed
based on the date when they were added
('http://shamela.ws/index.php/search/last/')
to make a list of all urls to be scraped.
Data collected:
* bookTitle
* bookUrl
* bok_file_URL
* dateAdded
This list is then saved as a csv file.
"""


import csv
import datetime
import json
import os
import re
import requests

from bs4 import BeautifulSoup



months = {
          "ديسمبر": 12,
          "نوفمبر": 11,
          "أكتوبر": 10,
          "سبتمبر": 9,
          "أغسطس": 8,
          "يوليو": 7,
          "يونيو": 6,
          "مايو": 5,
          "إبريل": 4,
          "مارس": 3,
          "فبراير": 2,
          "يناير": 1
          }


def format_shamela_date(html_date):
    """format the date from the Shamela page
    in Python's datetime format (YYYYMMDD)
    to be able to compare dates.

    Args:
        html_date (str): date of addition of a book on the Shamela website.
            The shamela dates are in the following format:
            "أضيف بتاريخ: 24 مايو 2019 م - عدد المشاهدات: 11807"

    Returns:
        date (datetime object)
        
    """
    html_date = html_date.split(": ")[1]
    for m in months:
        if m in html_date:
            html_date = html_date.replace(m, str(months[m]))
    date_list = html_date.split(" ")
    
    # date in yyyy/mm/dd format:
    date = datetime.datetime(int(date_list[2]),
                             int(date_list[1]),
                             int(date_list[0])
                             )
    return date


def get_last_page_of_results(url):
    """Get the last page of results from the footer of the page:
    <a href="/index.php/search/last/page-76">الأخير</a>

    Args:
        url (str): the url of the page where Shamela lists its books
            in order of addition to the website

    Returns:
        last_page_no (int): the last page of results
    """
    raw_html = requests.get(url, timeout=60)
    html = BeautifulSoup(raw_html.content, 'html.parser')
    a = html.find_all('a', text="الأخير")
    last_link = a[0]["href"]
    last_page_no = re.findall("page-(\d+)", last_link)[0]
    return int(last_page_no)
    

def scrape_shamela(csv_pth, not_before_date=()):
    """Write a csv with the title, bookurl, bok file url and date 
    of every book in Shamela.
    Optionally, give a cut-off date before which books will not be listed.

    Args:
        csv_pth (str): The path to the location where the csv file should be saved
        not_before_date (tuple): date (in format (YYYY, MM, DD));
            if a book was added to Shamela before this date,
            it should not be included in the csv
    
    Returns:
        None
    """
    url = 'http://shamela.ws/index.php/search/last/'
    base_url = 'http://shamela.ws'
    last_result_page = get_last_page_of_results(url)
    print("Last page of results: ", last_result_page)
    print("Currently scraping page: ")
    if not_before_date:
        not_before_date = datetime.datetime(*not_before_date)
    with open(csv_pth, 'w', encoding="utf-8") as f:
        header = ['bookID', 'bookTitle', 'bookUrl', 'bok_file_Url', 'pdf_file_Url', 'dateAdded']
        writer = csv.DictWriter(f, fieldnames=header, delimiter=",")
        writer.writeheader()

        for p in range(1,last_result_page+1):
            print(p)
            #print(url+'page-'+str(p))
            raw_html = requests.get(url+'page-'+str(p), timeout=60)
            html = BeautifulSoup(raw_html.content, 'html.parser')
            booksCollections = []
            bok_file_Url = []
            indexContainer = html.find('table')
            rows = indexContainer.find_all('tr')
        
            for row in rows:
                for cols in row.find_all('td', attrs={'class': 'regular-book'}):
                
                    book = {}
                    #print(cols)
                    try: # does not work with me (PV)
                        bookUrls = cols.find('a').get_attribute_list('href')[0]
                    except:
                        bookUrls= cols.find_all('a', href=True)[0]["href"]
                    bookID = bookUrls.split("/")[-1]
                    bookTitles = cols.find('a').text
                    dateAdded = cols.find_all('span')[0].text
                    dateAdded = format_shamela_date(dateAdded)
                    #print(bookTitles)
                    #input(dateAdded)
                    book['bookID']= bookID
                    book['bookTitle']= bookTitles
                    book['bookUrl']= base_url+bookUrls
                    book['dateAdded'] = dateAdded.strftime("%Y-%m-%d") # YYYY-MM-DD format
                    if not_before_date:
                        if dateAdded > not_before_date:
                            booksCollections.append(book)
                    else:
                        booksCollections.append(book)
                    #print(book)

            for item in booksCollections:
                #print(item['bookUrl'])
                page_row_file = requests.get(item['bookUrl'])
                page_html = BeautifulSoup(page_row_file.content, 'html.parser')
                
                #Since there was no div class or style, the bok image was targeted
                tags = page_html.find_all('img', {'src':'/files/img/front/bok.png'})
                for previous_tag in tags:
                    #link = previous_tag.findPrevious('a').get_attribute_list('href')[0]
                    link = previous_tag.findPrevious('a')["href"]
                    item['bok_file_Url'] = link
                    #print(base_url+link)
                try:
                    tags = page_html.find_all('img', {'src':'/files/img/front/pdf.png'})
                    for previous_tag in tags:
                        link = previous_tag.findPrevious('a')["href"]
                        item['pdf_file_Url'] = link
                except:
                    item['pdf_file_Url'] = ""

                writer.writerow(item)


today = datetime.datetime.now().strftime("%Y-%m-%d")
csv_pth = '0_shamela_scraping/shamelaScrapeList_{}.csv'.format(today)
scrape_shamela(csv_pth, not_before_date=(2011, 12, 31))
