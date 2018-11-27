import requests
import datetime
from html.parser import HTMLParser
from string import Template

class MyHTMLParser(HTMLParser):
    parsedString = ''
    tags = []
    thingsWeCareAbout = ['Score/min', 'K/D', 'Kills/min', 'Win %']
    currentDataKey = ''
    bfData = {'Date': datetime.datetime.today().strftime('%m/%d/%Y')}

    def handle_starttag(self, tag, attrs):

        if tag == 'div':
            for attr in attrs:
                for str in attr:
                    if str is not None:
                        if 'lifetime' in str:
                            self.tags.append(tag)

        if len(self.tags) > 0:
            self.tags.append(tag)

    def handle_endtag(self, tag):
        if len(self.tags) > 0:
            self.tags.pop()

    def handle_data(self, data):
        if 'Top Class' in data:
            self.tags = []

        if len(self.tags) > 0 and ('Top' not in data and 'Play Time' not in data):
            if self.tags[-1] == 'span':
                self.parsedString += self.tags[-1] + ' : ' + data.strip() + '\n'

                if self.currentDataKey in self.thingsWeCareAbout:
                    self.bfData[self.currentDataKey] = data.strip()

                self.currentDataKey = data.strip()


def main():
    proxy = ''

    proxy_dict = {
        "http": proxy,
        "https": proxy,
        "ftp": proxy
    }

    url_template = Template('https://battlefieldtracker.com/bfv/profile/origin/$userTag/overview')

    bfv_tag = input('Enter bfv username / gamer tag: ')

    url = url_template.substitute(userTag=bfv_tag)

    if proxy == '':
        html = requests.get(url).text
    else:
        html = requests.get(url, proxies=proxy_dict).text

    parser = MyHTMLParser()
    parser.feed(html)

    print(parser.bfData)


if __name__ == "__main__":
    main()
