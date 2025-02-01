import requests
from bs4 import BeautifulSoup
from converter import convert_month
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime
import datetime


class Parser:

    def parse(self, url):
        request = requests.get(url)
        if request.status_code != 200:
            raise 'Error occurred while reading the URL'
        soup = BeautifulSoup(request.content, 'html.parser')
        self.soup = soup
    
    @property
    def title(self):
        selector = '#dailyNewsPageHead > div.dailyNewsPageHead__description > h1'
        title = self.soup.select_one(selector)
        return title.text
    
    @property
    def date(self):
        selector = '#dailyNewsPageHead > div.dailyNewsPageHead__description > div.dailyNewsPageHead__description--tools > div > span'
        date = self.soup.select_one(selector)
        date, time = date.text.split(' | ')
        hour, min = map(digits.fa_to_en, time.split(':'))
        day, month, year = date.split()
        year, day = map(digits.fa_to_en, [year, day])
        month = convert_month(month=month)
        miladi = JalaliDateTime(int(year),int(month),int(day), int(hour), int(min)).to_gregorian()
        return miladi

    @property
    def body(self):
        div = self.soup.find('div', attrs={"class": "articlePost"})
        body = [s.extract() for s in div(['h2', 'p'])]
        text = ''
        for tag in body:
            text = text + tag.text + '\n' 
        
        return text




if __name__ == '__main__':
    par = Parser()
    par.parse('https://digiato.com/artificial-intelligence/silicon-valley-leaders-react-to-their-new-rival-deepseek')
    print(par.title)
    print(par.date)
    print(par.body)

