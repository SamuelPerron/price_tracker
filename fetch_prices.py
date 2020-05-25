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

    def locate_bestbuy(self, url):
        r = requests.get(url, headers={
            'Host': 'www.bestbuy.ca',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': 'CS_Culture=en-CA; nps={"currentUrlPath":"/en-ca/product/nintendo-switch-console-with-neon-red-blue-joy-con/13817625","hasSurveyBeenDisplayed":false,"heartBeat":1590420828,"isInSampling":false,"pageViewCount":1,"surveyLastDisplayed":1590149072}; AMCV_D6E638125859683E0A495D2D%40AdobeOrg=-1303530583%7CMCIDTS%7C18408%7CMCMID%7C48780787007354536658526858745383598070%7CMCAID%7CNONE%7CMCOPTOUT-1590428035s%7CNONE%7CvVersion%7C3.3.0%7CMCAAMLH-1591025635%7C7%7CMCAAMB-1591025635%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCCIDH%7C146324672; s_ecid=MCMID%7C48780787007354536658526858745383598070; criteoVisitorId=2196de1c-a32b-40e5-8d63-a7b5ad43c384; clientId=7cJMdgth4fIjmw3d; mbox=PC#63edc2101c3246059dfdc573337f545b.28_0#1653634357|session#e1e2962d201a452fb053a013b509b302#1590422687; ai_user=d9afr|2020-04-20T14:47:21.557Z; s_fid=48DDF21147627A62-00E95FE119CB37DD; s_lv=1590389556451; s_getNewRepeat=1590389556454-Repeat; _gcl_au=1.1.722746232.1587394045; aam_uuid=48290510961603513488566737109969328739; _ga=GA1.2.2101790875.1587394046; BVBRANDID=6cb45f3e-3465-464f-b69c-0251cb49be91; cto_bundle=47SX9F9SdGt1bSUyRml6VWU5eDA0UCUyQlV6V2N2NHZGJTJGWElFS2JoTzNHZ3p4RnU0WFJKMzY4NFAlMkJRcXVIWk5OejlQYTRhdno0ZlFpVDJ5TTg1R1NrOE0xNWZNRVBxNktLYjcwbjJwdkF5YzIlMkY5eFJsb0xINk9XYko0akdQSTRmelklMkJhOW80U0U1a2c1WjZKVkxqV2R2ZXVjb1FTaHR0WmlvdjdpVWpvanUlMkIlMkIlMkJPJTJCMWQ1dVJQYnJKOGdhZnRzN0RkNXI4NFVqeA; dtmEMI=U0FNVUVMUEVSUk9OQEhPVE1BSUwuRlI%253D; s_vnum=1590984000361%26vn%3D3; _pin_unauth=M2FjZjYzOTktMDZmZC00Y2JiLWJmNzktOTk0MmUxOGZmNmNk; rxVisitor=1590151952142ECL2SBKO6Q0TT8U85BHB255PG4E5EFJ0; dtPC=1$420824661_421h-vHBVHMBNFJIDIHPRUDKHSVHHKERAHMFAH-0; rxvt=1590422632315|1590420824667; dtSa=true%7CKD%7C-1%7CPage%3A%2013817625%7C-%7C1590421074094%7C420824661_421%7Chttps%3A%2F%2Fwww.bestbuy.ca%2Fen-ca%2Fproduct%2Fnintendo-switch-console-with-neon-red-blue-joy-con%2F13817625%7CNintendo%20Switch%20Console%20with%20Neon%20Red%2FBlue%20Joy-Con%20%5Ep%20Best%20Buy%20Canada%7C1590420828274%7C%7C; dtLatC=4; enabled=1; ReturnUrl=https://www.bestbuy.ca/; surveyOptOut=1; AMCVS_D6E638125859683E0A495D2D%40AdobeOrg=1; check=true; dtm_mSession=21003ca0c7cc406c99d54cf7c37c1aae; s_cc=true; _gid=GA1.2.1063195310.1590389541; s_sq=%5B%5BB%5D%5D; ak_bmsc=14D41BF7DF0202D07B7FD6AD98CDBD7CB89660B6DB5B000058E5CB5EB346BF0E~plioY60DtTGYjhTA7ZYnM11NbYGE/VWB/o0vVUL5BHEuLDBrDaihKiKXU6wnjxTRG60byGpRBf3KytkYA/3EQkfVP0GSrA9IJIf3gRDP6dynIVY67JyCy4PuCzzhF2LRByJzy9X/CfenipNN7HFiP789clWVawbDPAkCaiQKLwpfYlUJsPGc+t58FP9RFTDGLG42GtRXIflN9u+SbdeHsvb80zrxnVyC4UVABmG9EVSrEjE0WWqzIBPnX4JKFSyY8C; ai_session=nwWoZ|1590420826844|1590420826844; bm_sv=4A4F7E95F55CF460F49F5EE211165C22~IJb9bRF5vOqCUbBHf64u6/WJtuNrBaFPJz4HEwKe3ibsrzcP1qM6ZLltGsw8UGjmpfX/3CaUwIPcKSsUlRLq6WFdLZvzW2C6BtY1ggkKHllXQYUZSrg7f7vxGYU2CQGici1kfJ+kazPbXjGTyaeJnEL16h9sprm9dB8XF2TpkaQ=; dtCookie=1$8984DD26BD17841C773DC3A1B5C54529|ea7c4b59f27d43eb|0',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        price_str = soup.find('meta', {'itemprop': 'price'})
        cart_btn = soup.find('button', {'class': 'addToCartButton_1DQ8z'})
        store_btn = soup.find('button', {'class': 'x-reserveInStoreButton'})
        try:
            test = cart_btn['disabled']
            test = store_btn['disabled']
            return None
        except KeyError:
            if not price_str:
                return None
            else:
                return float(price_str['content'])

    def find_price(self, item):
        found = None
        if item['website'] == 'amazon':
            found = self.locate_amazon(item['url'])
        elif item['website'] == 'playstation':
            found = self.locate_playstation(item['url'])
        elif item['website'] == 'bestbuy':
            found = self.locate_bestbuy(item['url'])

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
