from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod


class Crawler(ABC):

    @abstractmethod
    def __init__(self, past_hour=1, topic=['tech', ]):
        pass

    @property
    @abstractmethod
    def url(self):
        pass


class DigiatoCrawler(Crawler):

    def __init__(self, past_hour=1, topic=['tech', ]):
        self.past_hour = past_hour
        self.topic = topic
        self.URL = 'https://digiato.com/topic/tech'

    @property
    def url(self):
        request = requests.get(self.URL)
        if request.status_code != 200:
            raise 'Failed to load url'
        soup = BeautifulSoup(request.content, 'html.parser')

        links = soup.find_all('a', attrs={"class": "rowCard__title"})

        print(len(links))
        for link in links:
            print(link['href'])


if __name__ == '__main__':
    craw = DigiatoCrawler()
    craw.url
