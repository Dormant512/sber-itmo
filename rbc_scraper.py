from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta, datetime
import csv
import re
from requests_html import HTMLSession


def daterange(start_date, end_date):
    """Yields a range of dates to iterate (inluding end)."""
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


start_date = date(2020, 1, 1)
end_date = date(2020, 9, 30)


def get_news_from_date(cur_date):
    """Returns all news titles from RBC.RU from a given date range."""
    rus_months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    date_url = cur_date.strftime("%d.%m.%Y")

    url = f"https://www.rbc.ru/search2/?query=&dateFrom={date_url}&dateTo={date_url}"
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=360)
    print("Html rendered.", end='\r')

    soup = BeautifulSoup(r.html.html, 'html.parser')
    divs = soup.find_all('div', class_="search-item js-search-item")

    cur_titles = []
    #dates = []
    for num, item in enumerate(divs):
        title = item.find('span', class_="search-item__title").text.strip()
        #date_raw = item.find('span', class_="search-item__category").text.strip()
        #match = re.search(r'\d{2} \w{3} \d{4}', date_raw)
        #dt_items = match.group(1, 2, 3)
        #date = date(int(dt_items[2]), int(rus_months.index(dt_items[1]) + 1), int(dt_items[0]))
                
        cur_titles.append(title)
        #dates.append(date)

    return cur_titles


if __name__ == "__main__":

        with open(f"sber_work_files/rbc_news.csv", 'w', newline='') as csvfile:
            news_writer = csv.writer(csvfile, delimiter='\t', quotechar='"', \
                    quoting=csv.QUOTE_ALL, skipinitialspace=True)
            news_writer.writerow(["date", "title"])

            for single_date in daterange(start_date, end_date):
                cur_news = get_news_from_date(single_date)
                print(f"News for {single_date} scraped.")

                for title in cur_news:
                    news_writer.writerow([single_date] + [title])

