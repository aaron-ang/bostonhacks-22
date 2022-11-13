# pip install requests
# pip install html5lib
# pip install bs4

import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta
import csv


def returnListUrls():
    today = date.today()
    # print("d = ", d)
    list_days = []
    for i in range(0, 7):
        day = today + timedelta(days=i)
        list_days.append(day)

    list_urls = []
    for i in range(len(list_days)):
        url = "https://www.bu.edu/calendar/?day=" + \
            list_days[i].strftime("%Y-%m-%d")
        # print(url)
        list_urls.append(url)
    return list_urls


def returnEventUrls():
    list_raw_urls = returnListUrls()
    list_full_urls = []
    for url in list_raw_urls:
        temp = []
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        event_list = soup.find('section', id="event-list")
        # print(event_list.findAll('li'))

        list_day_urls = []
        for tag in event_list.findAll('li'):
            temp.append(str(tag))

        for event in temp:
            event = event.split("/calendar/?")[1]
            event = event.split("&amp;day")[0]
            event = url+"&"+event
            list_day_urls.append(event)
            # print(event)

        list_full_urls.append(list_day_urls)

    return list_full_urls


def getEvents():
    list_full_urls = returnEventUrls()
    url = list_full_urls[0][0]

    database = []
    count = 0
    for list_day_url in list_full_urls:
        for url in list_day_url:
            database.append(inputElement(url))

    # CHANGE PATH
    PATH = "C:/Users/etanm/OneDrive/Documents/VSCode/BostonHacks/data.csv"
    with open(PATH, 'w', newline='') as csvfile:
        fieldnames = ['url', 'title', 'details', 'time', 'org']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for list in database:
            try:
                writer.writerow(
                    {'url': list[0], 'title': list[1], 'details': list[2], 'time': list[3], 'org': list[4]})
            except:
                pass


def inputElement(url):
    db_item = [(url)]

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    # print(soup)
    event = soup.find('section', id='event-detail')

    title = event.find('h1')
    # print(str(title))
    title = str(title)
    try:
        title = title.split("<h1>")[1]
    except:
        pass
    title = title.split("</h1>")[0]
    # print(title)
    db_item.append((title))

    details = event.find('p')
    # print(str(details))
    details = str(details)
    details = details.split("<p>")[1]
    details = details.split("</p>")[0]
    # print(details)
    db_item.append((details))

    raw_th = event.findAll('th')
    for i in range(len(raw_th)):
        raw_th[i] = str(raw_th[i]).split("<th>")[1]
        raw_th[i] = raw_th[i].split("</th>")[0]

    raw_td = event.findAll('td')
    for i in range(len(raw_th)):
        raw_td[i] = str(raw_td[i]).split("<td>")[1]
        raw_td[i] = raw_td[i].split("</td>")[0]

    table = dict(zip(raw_th, raw_td))
    # print(table)

    db_item.append(table['When'])
    try:
        db_item.append(table['Contact Organization'])
    except:
        db_item.append("")
    # print(db_item)

    return db_item


getEvents()
