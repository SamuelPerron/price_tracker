from bs4 import BeautifulSoup
import requests
import csv
import re

class PriceTracker():
    items = []

    def __init__(self):
        with open('products.csv', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.items.append({
                    'name': row[0],
                    'url': row[1],
                    'website': self.find_website(row[1]),
                    'first_price': float(row[2]),
                    'target_price': float(row[3]),
                    'actual_price': 0,
                    'is_na': False,
                })

    def find_website(self, url):
        return re.search("http://|https://.+[a-z]\.", url).group().split('.')[1]

    def locate_amazon(self, url):
        r = requests.get(url, headers={
            'Host': 'www.amazon.ca',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'session-id=130-7107170-7241238; session-id-time=2082787201l; i18n-prefs=CAD; csm-hit=tb:s-8XGZFA33TWSW93AT2EZC|1590418401372&t:1590418403742&adb:adblk_no; ubid-acbca=131-2041366-3868558; session-token=Qa1ni/O/FqGFua15TESm8qrmdOwNjwLxAROYkYTiV5zvbn70ocXz63w2WlFC4HvVExHkq5XrWYcC4fUXeuM5OSnWOWQRGaR8anXK/ugYFRmX1lgn0z5TD7aaOVEV/n7BCBQSN5BLiMOWEDFZUicaREtHTzC/bZTlr1Dj8q6KepKunKVsxS+r2gq4xc4E7F12G50yJxCHsfr7DYnT5Bhm//UT4eI6MJX2ph6gAG6ofkmjh2Tz3eSjS9v6HEp9LNO/OgoY4YsFTHc=; x-wl-uid=10zp855f9okYwCTKnHgBV3xqulQgvyK/0IcHPeN1e7klpxpim3jAe7OkGuz87yoBo2fPQqpaKtuw=',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        price_str = soup.find(id='priceblock_ourprice')
        if not price_str:
            return None
        else:
            for i in price_str.get_text().split('CDN$'):
                if i != '':
                    return float(i.strip().replace(',', '.'))

    def locate_playstation(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_str = soup.find('h3', {'class': 'price-display__price'})
        if not price_str:
            return None
        else:
            for i in price_str.get_text().split('$'):
                if i != '':
                    return float(i.strip())

    def find_price(self, item):
        found = None
        if item['website'] == 'amazon':
            found = self.locate_amazon(item['url'])
        elif item['website'] == 'playstation':
            found = self.locate_playstation(item['url'])

        if found:
            item['actual_price'] = found
        else:
            item['is_na'] = True

    def fetch_prices(self):
        i = 0
        for item in self.items:
            self.find_price(self.items[i])
            self.print_price(self.items[i])
            i += 1

    def calculate_diff(self, item):
        return round(((item['actual_price'] - item['first_price']) / ((item['actual_price'] + item['first_price']) / 2)) * 100, 2)

    def print_price(self, item):
        if not item['is_na']:
            print(f"{item['website']} | {item['name']} ----- {item['actual_price']} $ ({self.calculate_diff(item)}%)")
        else:
            print(f"{item['website']} | {item['name']} ----- N/A")


tracker = PriceTracker()
tracker.fetch_prices()
