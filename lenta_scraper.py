from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import csv


def daterange(start_date, end_date):
    """Yields a range of dates to iterate (inluding end)."""
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


start_date = date(2020, 1, 1)
end_date = date(2020, 9, 30)


def get_news_from_date(cur_date):
    """Returns all news titles from LENTA.RU from a given date."""
    date_url = cur_date.strftime("%Y/%m/%d")

    url = f"https://lenta.ru/rubrics/russia/{date_url}/"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    sections = soup.find_all('a', class_="card-full-news _archive")

    cur_titles = []
    for item in sections:
        title = item.find('h3', class_="card-full-news__title").text.strip()
        cur_titles.append(title)

    return cur_titles


if __name__ == "__main__":

    with open('lenta_news.csv', 'w', newline='') as csvfile:
        news_writer = csv.writer(csvfile, delimiter='\t', quotechar='"', \
                quoting=csv.QUOTE_ALL, skipinitialspace=True)
        news_writer.writerow(["date", "title"])

        for single_date in daterange(start_date, end_date):
            cur_news = get_news_from_date(single_date)
            print(f"News for {single_date} scraped.")
            
            for title in cur_news:
                news_writer.writerow([single_date] + [title])
    
